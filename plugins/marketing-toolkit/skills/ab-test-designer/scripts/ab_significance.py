#!/usr/bin/env python3
"""
Test statistical significance of an A/B test result.

Usage (proportions — CTR, conv rate):
    python3 ab_significance.py --a-total 10000 --a-converted 200 --b-total 10000 --b-converted 240

Usage (continuous — revenue, time on page; provide means + std):
    python3 ab_significance.py --continuous --a-n 200 --a-mean 15.0 --a-std 4.5 --b-n 205 --b-mean 17.2 --b-std 5.1
"""
import argparse
import math
import sys


def _z_score(p):
    if p <= 0 or p >= 1:
        raise ValueError("p must be in (0, 1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_low, p_high = 0.02425, 1 - 0.02425
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)


def _norm_cdf(z):
    """Standard normal CDF — Abramowitz & Stegun approx, ~5 decimal accuracy."""
    # For z values, compute using error function approximation
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def two_proportion_z_test(a_total, a_conv, b_total, b_conv, alpha=0.05):
    """Two-proportion z-test, two-sided."""
    p1 = a_conv / a_total
    p2 = b_conv / b_total
    p_pooled = (a_conv + b_conv) / (a_total + b_total)
    se = math.sqrt(p_pooled * (1 - p_pooled) * (1/a_total + 1/b_total))
    if se == 0:
        z = float("inf") if p1 != p2 else 0
    else:
        z = (p2 - p1) / se
    # Two-sided p-value
    p_value = 2 * (1 - _norm_cdf(abs(z)))
    return {
        "p1": p1, "p2": p2,
        "lift_abs": p2 - p1,
        "lift_rel": (p2 - p1) / p1 if p1 else 0,
        "z": z,
        "p_value": p_value,
        "significant": p_value < alpha,
        "winner": "B" if p2 > p1 and p_value < alpha else ("A" if p1 > p2 and p_value < alpha else "inconclusive"),
    }


def welch_t_test(a_n, a_mean, a_std, b_n, b_mean, b_std, alpha=0.05):
    """Welch's t-test (unequal variance)."""
    se = math.sqrt(a_std**2 / a_n + b_std**2 / b_n)
    if se == 0:
        t = float("inf") if a_mean != b_mean else 0
    else:
        t = (b_mean - a_mean) / se
    # Welch-Satterthwaite degrees of freedom
    df_num = (a_std**2/a_n + b_std**2/b_n) ** 2
    df_den = (a_std**2/a_n)**2 / (a_n - 1) + (b_std**2/b_n)**2 / (b_n - 1) if (a_n > 1 and b_n > 1) else 1
    df = df_num / df_den if df_den > 0 else max(a_n + b_n - 2, 1)
    # Approximate p-value using normal for large df
    p_value = 2 * (1 - _norm_cdf(abs(t)))
    return {
        "a_mean": a_mean, "b_mean": b_mean,
        "lift_abs": b_mean - a_mean,
        "lift_rel": (b_mean - a_mean) / a_mean if a_mean else 0,
        "t": t, "df": df,
        "p_value": p_value,
        "significant": p_value < alpha,
        "winner": "B" if b_mean > a_mean and p_value < alpha else ("A" if a_mean > b_mean and p_value < alpha else "inconclusive"),
    }


def format_result_proportions(r, a_total, b_total, alpha=0.05):
    out = []
    out.append("# A/B Test Significance Result (proportions)\n")
    out.append(f"**A** converted at **{r['p1']*100:.2f}%** ({a_total:,} total)")
    out.append(f"**B** converted at **{r['p2']*100:.2f}%** ({b_total:,} total)")
    out.append(f"\n**Absolute lift:** {r['lift_abs']*100:+.2f} pp")
    out.append(f"**Relative lift:** {r['lift_rel']*100:+.1f}%")
    out.append(f"\n**Z-score:** {r['z']:.3f}")
    out.append(f"**p-value:** {r['p_value']:.4f}")
    out.append(f"**Significance threshold:** α = {alpha}")

    out.append("\n## Verdict")
    if r['significant']:
        if r['winner'] == 'B':
            out.append(f"✅ **Significant WIN for B.** Ship B. (p={r['p_value']:.4f} < {alpha})")
        else:
            out.append(f"🔴 **Significant LOSS for B.** Keep A. Log the learning. (p={r['p_value']:.4f} < {alpha})")
    else:
        out.append(f"⚪ **INCONCLUSIVE.** p-value {r['p_value']:.4f} ≥ {alpha}.")
        out.append("  - Either the real difference is smaller than what this sample can detect,")
        out.append("  - OR you haven't collected enough data yet.")
        out.append("  - Check sample size with `sample_size.py` — run longer if needed.")

    # Sample size sanity check
    min_n = 1000 / max(r['p1'], 0.001)  # very rough
    if min(a_total, b_total) < 1000:
        out.append(f"\n⚠️  **Underpowered** — each variant has <1000 samples. Result may be unreliable even if p<0.05.")

    out.append("\n## Pitfalls to verify")
    out.append("- Did you peek at results and stop early? (Inflates false-positive rate)")
    out.append("- Did traffic split stay ~50/50 throughout? (SRM check)")
    out.append("- Was the test period free of anomalies (holidays, outages, campaign changes)?")
    return "\n".join(out)


def format_result_continuous(r, a_n, b_n, alpha=0.05):
    out = []
    out.append("# A/B Test Significance Result (continuous)\n")
    out.append(f"**A mean:** {r['a_mean']:.2f} (n={a_n:,})")
    out.append(f"**B mean:** {r['b_mean']:.2f} (n={b_n:,})")
    out.append(f"\n**Absolute lift:** {r['lift_abs']:+.2f}")
    out.append(f"**Relative lift:** {r['lift_rel']*100:+.1f}%")
    out.append(f"\n**t-stat:** {r['t']:.3f}")
    out.append(f"**df:** {r['df']:.1f}")
    out.append(f"**p-value:** {r['p_value']:.4f}")
    out.append(f"\n## Verdict")
    if r['significant']:
        if r['winner'] == 'B':
            out.append(f"✅ **Significant WIN for B.** Ship B.")
        else:
            out.append(f"🔴 **Significant LOSS for B.** Keep A.")
    else:
        out.append(f"⚪ **INCONCLUSIVE.** Run longer or accept no difference.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--continuous", action="store_true", help="Use t-test (continuous metric)")
    # Proportions
    p.add_argument("--a-total", type=int)
    p.add_argument("--a-converted", type=int)
    p.add_argument("--b-total", type=int)
    p.add_argument("--b-converted", type=int)
    # Continuous
    p.add_argument("--a-n", type=int)
    p.add_argument("--a-mean", type=float)
    p.add_argument("--a-std", type=float)
    p.add_argument("--b-n", type=int)
    p.add_argument("--b-mean", type=float)
    p.add_argument("--b-std", type=float)
    p.add_argument("--alpha", type=float, default=0.05)
    args = p.parse_args()

    if args.continuous:
        if None in (args.a_n, args.a_mean, args.a_std, args.b_n, args.b_mean, args.b_std):
            print("Continuous test requires --a-n --a-mean --a-std --b-n --b-mean --b-std")
            sys.exit(1)
        r = welch_t_test(args.a_n, args.a_mean, args.a_std, args.b_n, args.b_mean, args.b_std, args.alpha)
        print(format_result_continuous(r, args.a_n, args.b_n, args.alpha))
    else:
        if None in (args.a_total, args.a_converted, args.b_total, args.b_converted):
            print("Proportions test requires --a-total --a-converted --b-total --b-converted")
            sys.exit(1)
        r = two_proportion_z_test(args.a_total, args.a_converted, args.b_total, args.b_converted, args.alpha)
        print(format_result_proportions(r, args.a_total, args.b_total, args.alpha))


if __name__ == "__main__":
    main()
