"""
Runs a single scenario through either system, wraps it with timing, and
attaches the scenario's ground-truth metadata for downstream analysis.
"""
import time

from src.agent_baseline import run_baseline
from src.agents_treatment import run_treatment
from src.llm_client import LLMClient
from src.scenarios import Scenario


def run_scenario(scenario: Scenario, system: str, client: LLMClient) -> dict:
    start = time.time()
    if system == "baseline":
        result = run_baseline(scenario, client)
    elif system == "treatment":
        result = run_treatment(scenario, client)
    else:
        raise ValueError(f"Unknown system: {system!r}")
    result["completion_time_s"] = time.time() - start

    result["injected_violation"] = scenario.injected_violation
    result["violation_type"] = scenario.violation_type
    result["category"] = scenario.category
    result["urgency"] = scenario.urgency
    result["requires_signoff"] = scenario.requires_signoff
    return result