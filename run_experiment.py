#!/usr/bin/env python
"""
Runs every scenario through both systems, logs to CSV, prints comparison.
"""
import argparse
import sys

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from src.llm_client import LLMClient
from src.metrics import paired_significance, summarise
from src.orchestrator import run_scenario
from src.scenarios import build_scenarios


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--out", type=str, default="outputs/results.csv")
    args = parser.parse_args()

    client = LLMClient()
    scenarios = build_scenarios()
    rows = []
    total_runs = len(scenarios) * 2 * args.repeats
    done = 0

    for rep in range(args.repeats):
        for scenario in scenarios:
            for system in ("baseline", "treatment"):
                result = run_scenario(scenario, system, client)
                result["repeat"] = rep
                rows.append(result)
                done += 1
                print(f"[{done}/{total_runs}] {scenario.id:>3} via {system:<9} — "
                      f"{result['completion_time_s']:.2f}s, "
                      f"{result['agent_interactions']} interactions, "
                      f"violation_occurred={result['violation_occurred']}")

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)
    print(f"\nRaw results written to {args.out}\n")
    print("=== Summary ===")
    print(summarise(df).to_string(index=False))

    if args.repeats == 1:
        print("\n=== Paired significance (baseline vs treatment) ===")
        for k, v in paired_significance(df).items():
            print(f"{k}: {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())