from dotenv import load_dotenv
load_dotenv()

from src.scenarios import build_scenarios
from src.llm_client import LLMClient
from src.agent_baseline import run_baseline

client = LLMClient()
scenarios = build_scenarios()

# Test one normal ticket and one violation-attempt ticket
normal = next(s for s in scenarios if s.id == "N01")
violation = next(s for s in scenarios if s.id == "V01")

for scenario in [normal, violation]:
    print(f"--- {scenario.id} ({scenario.violation_type or 'normal'}) ---")
    result = run_baseline(scenario, client)
    print(result["raw_result"])
    print("violation_occurred:", result["violation_occurred"])
    print()