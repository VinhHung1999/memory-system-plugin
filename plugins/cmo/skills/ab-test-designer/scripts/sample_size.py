#!/usr/bin/env python3
"""
Calculate minimum sample size per variant for an A/B test.

Usage:
    python3 sample_size.py --baseline-rate 0.02 --mde 0.10 --power 0.8 --alpha 0.05

Assumptions:
    - Two-sided test
    - Equal allocation (50/50)
    - Proportions (CTR, conversion rate) — uses normal approximation
"""
import argparse
import math


def sample_size_proportions(p1, mde_relative, alpha=0.05, power=0.8):
    """Sample size per variant for a two-proportion z-test.
    p1: baseline rate (control)
    mde_relative: minimum detectable effect as % of p1 (e.g., 0.10 = 10% relative lift)
    """
    # Z-scores
    # Two-sided
    z_alpha = _z_score(1 - alpha / 2)
    z_beta = _z_score(power)

    p2 = p1 * (1 + mde_relative)
    pbar = (p1 + p2) / 2

    numerator = (z_alpha * math.sqrt(2 * pbar * (1 - pbar)) +
                 z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2

    n = numerator / denominator
    return math.ceil(n)


def _z_score(p):
    """Inverse standard normal CDF. Uses rational approximation (no scipy)."""
    # Beasley-Springer-Moro approximation, good to ~4 decimal places for [0.001, 0.999]
    if p <= 0 or p >= 1:
        raise ValueError("p must be in (0, 1)")
    # Hastings approximation
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]

    p_low = 0.02425
    p_high = 1 - p_low

    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
               ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / \
               (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--baseline-rate", type=float, required=True,
                   help="Baseline conversion/click rate (e.g., 0.02 for 2 percent)")
    p.add_argument("--mde", type=float, required=True,
                   help="Minimum detectable effect as relative lift (0.10 = 10 percent)")
    p.add_argument("--power", type=float, default=0.8, help="Statistical power (default 0.8)")
    p.add_argument("--alpha", type=float, default=0.05, help="Significance level (default 0.05)")
    args = p.parse_args()

    n = sample_size_proportions(args.baseline_rate, args.mde, args.alpha, args.power)
    total = n * 2
    p1 = args.baseline_rate
    p2 = p1 * (1 + args.mde)

    print(f"# A/B Test Sample Size Calculator")
    print(f"\n**Baseline rate (A):** {p1*100:.2f}%")
    print(f"**Target rate (B) for MDE:** {p2*100:.2f}% ({args.mde*100:.0f}% relative lift)")
    print(f"**Power:** {args.power*100:.0f}%")
    print(f"**Alpha:** {args.alpha}")
    print(f"\n**Minimum per variant:** {n:,} visits/impressions")
    print(f"**Total test traffic needed:** {total:,}")
    print(f"\n## How long to run?")
    print(f"- If you get 1,000 visits/day → run ~{math.ceil(total/1000)} days")
    print(f"- If you get 500 visits/day → run ~{math.ceil(total/500)} days")
    print(f"- If you get 10,000 visits/day → run ~{math.ceil(total/10000)} days")
    print(f"\n## Notes")
    print(f"- Plan duration upfront. Don't peek or stop early.")
    print(f"- If you can't hit this sample in a reasonable period, accept a bigger MDE (you can only detect larger effects) or run longer.")


if __name__ == "__main__":
    main()
