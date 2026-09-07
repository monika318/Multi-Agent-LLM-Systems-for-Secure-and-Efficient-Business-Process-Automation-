"""
Descriptive statistics and paired significance tests.

- Wilcoxon signed-rank: paired, non-parametric — appropriate for a small-N
  paired comparison of completion time / interaction count (RQ2/H2).
- McNemar's test: paired binary outcomes (violation occurred: yes/no) on
  the same scenarios across two systems (RQ3/H1).
"""
import pandas as pd
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar


def summarise(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("system")
        .agg(
            n=("scenario_id", "count"),
            mean_completion_s=("completion_time_s", "mean"),
            mean_interactions=("agent_interactions", "mean"),
            violation_rate=("violation_occurred", "mean"),
        )
        .reset_index()
    )


def paired_significance(df: pd.DataFrame) -> dict:
    out = {}
    pivot_time = df.pivot(index="scenario_id", columns="system", values="completion_time_s")
    pivot_inter = df.pivot(index="scenario_id", columns="system", values="agent_interactions")

    try:
        w_time = stats.wilcoxon(pivot_time["baseline"], pivot_time["treatment"])
        out["completion_time_wilcoxon_p"] = round(float(w_time.pvalue), 4)
    except Exception as e:
        out["completion_time_wilcoxon_p"] = f"n/a ({e})"

    try:
        w_inter = stats.wilcoxon(pivot_inter["baseline"], pivot_inter["treatment"])
        out["interactions_wilcoxon_p"] = round(float(w_inter.pvalue), 4)
    except Exception as e:
        out["interactions_wilcoxon_p"] = f"n/a ({e})"

    viol = df[df["injected_violation"]]
    pivot_v = viol.pivot(index="scenario_id", columns="system", values="violation_occurred")
    a = int(((~pivot_v["baseline"]) & (~pivot_v["treatment"])).sum())
    b = int(((pivot_v["baseline"]) & (~pivot_v["treatment"])).sum())
    c = int(((~pivot_v["baseline"]) & (pivot_v["treatment"])).sum())
    d = int(((pivot_v["baseline"]) & (pivot_v["treatment"])).sum())
    table = [[a, b], [c, d]]

    try:
        result = mcnemar(table, exact=True)
        out["mcnemar_p"] = round(float(result.pvalue), 4)
    except Exception as e:
        out["mcnemar_p"] = f"n/a ({e})"

    out["violation_contingency_table"] = {
        "both_clean": a, "baseline_violated_only": b,
        "treatment_violated_only": c, "both_violated": d,
    }
    return out