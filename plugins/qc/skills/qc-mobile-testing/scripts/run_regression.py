#!/usr/bin/env python3
"""
Run all automation scripts in qc-workspace/flows/* and generate a regression summary.

Usage:
    python run_regression.py [--workspace ./qc-workspace] [--device emulator-5554]

Each automation-script.py in qc-workspace/flows/<flow>/ is executed with:
    --output-dir <workspace>/regression/<timestamp>/<flow>/

After all flows complete, a summary.html is generated at:
    <workspace>/regression/<timestamp>/summary.html
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import time
from datetime import datetime

# Make appium_lib importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from appium_lib import RegressionReporter


def find_flows(workspace):
    """Find all flows that have an automation-script.py."""
    pattern = os.path.join(workspace, "flows", "*", "automation-script.py")
    scripts = sorted(glob.glob(pattern))
    return [(os.path.basename(os.path.dirname(s)), s) for s in scripts]


def load_flow_config(workspace, flow_name):
    """Load optional flows.json with default args per flow."""
    config_path = os.path.join(workspace, "flows.json")
    if not os.path.exists(config_path):
        return []
    with open(config_path) as f:
        config = json.load(f)
    flow_config = config.get(flow_name, {})
    args = []
    for k, v in flow_config.items():
        args.extend([f"--{k}", str(v)])
    return args


def run_flow(flow_name, script_path, output_dir, device, port, extra_args):
    """Execute one automation script. Returns (return_code, duration_s)."""
    print(f"\n{'='*60}")
    print(f"  Running: {flow_name}")
    print(f"  Script:  {script_path}")
    print(f"  Output:  {output_dir}")
    print(f"{'='*60}")

    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        sys.executable, script_path,
        "--output-dir", output_dir,
        "--device", device,
        "--port", str(port),
    ] + extra_args

    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=False)
        duration = time.time() - start
        return result.returncode, duration
    except Exception as e:
        print(f"  ERROR: {e}")
        return 1, time.time() - start


def main():
    parser = argparse.ArgumentParser(description="Run regression suite for all flows.")
    parser.add_argument("--workspace", default="./qc-workspace",
                        help="Path to qc-workspace directory (default: ./qc-workspace)")
    parser.add_argument("--device", default="emulator-5554",
                        help="Device to run on (default: emulator-5554)")
    parser.add_argument("--port", type=int, default=4723,
                        help="Appium port (default: 4723)")
    parser.add_argument("--app", default=None,
                        help="App package name (auto-detect from flows.json if omitted)")
    parser.add_argument("--no-open", action="store_true",
                        help="Don't auto-open the summary HTML in browser")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    if not os.path.exists(workspace):
        print(f"ERROR: Workspace not found: {workspace}")
        sys.exit(1)

    flows = find_flows(workspace)
    if not flows:
        print(f"ERROR: No flows found in {workspace}/flows/*/automation-script.py")
        sys.exit(1)

    # Setup regression run directory
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    regression_dir = os.path.join(workspace, "regression", run_id)
    os.makedirs(regression_dir, exist_ok=True)

    # Detect app from first flows.json or fallback
    app = args.app or "unknown.app"

    print(f"\n  QC Regression Run #{run_id}")
    print(f"  Workspace: {workspace}")
    print(f"  Device:    {args.device}")
    print(f"  Flows:     {len(flows)}")
    for name, _ in flows:
        print(f"    - {name}")

    reporter = RegressionReporter(
        output_dir=regression_dir,
        app=app,
        device=args.device,
        run_id=run_id,
    )

    # Run each flow
    for flow_name, script_path in flows:
        flow_output = os.path.join(regression_dir, flow_name)
        flow_args = load_flow_config(workspace, flow_name)

        return_code, duration = run_flow(
            flow_name, script_path, flow_output,
            args.device, args.port, flow_args,
        )

        # Read result.json that the script wrote
        result_json = os.path.join(flow_output, "result.json")
        if os.path.exists(result_json):
            try:
                reporter.add_flow_from_result_json(
                    name=flow_name.replace("-", " ").title(),
                    flow_dir=flow_name,
                    result_json_path=result_json,
                )
            except Exception as e:
                print(f"  WARN: Could not read result.json: {e}")
                reporter.add_flow(
                    name=flow_name.replace("-", " ").title(),
                    flow_dir=flow_name,
                    status="fail" if return_code != 0 else "pass",
                    steps_passed=0,
                    steps_total=0,
                    duration_s=duration,
                    failure={"step_name": "—", "error": "result.json missing", "selector": ""},
                )
        else:
            # Script didn't write result.json — mark as failed
            reporter.add_flow(
                name=flow_name.replace("-", " ").title(),
                flow_dir=flow_name,
                status="fail",
                steps_passed=0,
                steps_total=0,
                duration_s=duration,
                failure={
                    "step_name": "Script execution",
                    "error": f"Script exited with code {return_code} and did not write result.json",
                    "selector": "",
                },
            )

    # Generate summary
    summary_path = reporter.write()

    print(f"\n{'='*60}")
    print(f"  Regression complete")
    print(f"  Summary: {summary_path}")
    print(f"{'='*60}\n")

    # Open in browser
    if not args.no_open:
        try:
            subprocess.run(["open", summary_path], check=False)
        except Exception:
            pass

    # Exit with non-zero if any flow failed
    failed = sum(1 for f in reporter.flows if f["status"] == "fail")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
