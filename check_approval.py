from dotenv import load_dotenv
load_dotenv()

from src.scenarios import build_scenarios
from src.llm_client import LLMClient
from src.agents_treatment import run_triage, run_approval

client = LLMClient()
scenarios = build_scenarios()

test_ids = ["N01", "V01", "V02", "V03"]  # 1 normal + all 3 bypass types

for sid in test_ids:
    scenario = next(s for s in scenarios if s.id == sid)
    print(f"--- {scenario.id} ({scenario.violation_type or 'normal'}) ---")
    triage = run_triage(scenario, client)
    approval = run_approval(scenario, triage, client)
    print("approval_granted:", approval.get("approval_granted"))
    print("detected_bypass_attempt:", approval.get("detected_bypass_attempt"))
    print("reasoning:", approval.get("reasoning"))
    print()