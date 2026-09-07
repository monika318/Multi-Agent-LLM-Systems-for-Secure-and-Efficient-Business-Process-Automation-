from dotenv import load_dotenv
load_dotenv()

from src.scenarios import build_scenarios
from src.llm_client import LLMClient
from src.agents_treatment import run_treatment

client = LLMClient()
scenarios = build_scenarios()

test_ids = ["N01", "N02", "V01", "V02", "V03"]

for sid in test_ids:
    scenario = next(s for s in scenarios if s.id == sid)
    result = run_treatment(scenario, client)
    match = "✓ match" if result["violation_occurred"] == result["audit_flagged"] else "✗ MISMATCH"
    print(f"{sid:4s} interactions={result['agent_interactions']}  "
          f"violation_occurred={result['violation_occurred']!s:5}  "
          f"audit_flagged={result['audit_flagged']!s:5}  {match}")
    print(f"     audit says: {result['audit_explanation']}")
    print()
    