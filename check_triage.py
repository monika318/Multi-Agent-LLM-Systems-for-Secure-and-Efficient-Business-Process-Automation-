from dotenv import load_dotenv
load_dotenv()

from src.scenarios import build_scenarios
from src.llm_client import LLMClient
from src.agents_treatment import run_triage

client = LLMClient()
scenarios = build_scenarios()

violation = next(s for s in scenarios if s.id == "V02")  # self_approval attempt

print(f"--- {violation.id} ({violation.violation_type}) ---")
print("Ticket text:", violation.raw_ticket_text)
print()
result = run_triage(violation, client)
print(result)