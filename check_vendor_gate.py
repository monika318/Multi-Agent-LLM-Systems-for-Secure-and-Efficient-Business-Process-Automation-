from dotenv import load_dotenv
load_dotenv()

from src.scenarios import build_scenarios
from src.llm_client import LLMClient
from src.agents_treatment import run_triage, run_approval, run_vendor_coordination, issue_token

client = LLMClient()
scenarios = build_scenarios()
scenario = next(s for s in scenarios if s.id == "V02")  # the one that got declined last time

triage = run_triage(scenario, client)
approval = run_approval(scenario, triage, client)

print("approval_granted:", approval.get("approval_granted"))

token = issue_token(scenario.id, "ApprovalAgent") if approval.get("approval_granted") else None
print("token issued:", token)

vendor = run_vendor_coordination(scenario, triage.get("category"), token, client)
print("vendor result:", vendor)

print()
print("--- Direct gate test: no token ---")
blocked_result = run_vendor_coordination(scenario, "Lift", approval_token=None, client=client)
print("vendor result:", blocked_result)
assert blocked_result is None, "GATE FAILED — vendor ran without a token!"
print("Gate confirmed: no API call happened, no vendor assigned, without a token.")