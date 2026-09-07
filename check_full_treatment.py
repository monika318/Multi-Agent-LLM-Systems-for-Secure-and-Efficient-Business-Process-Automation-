from dotenv import load_dotenv
load_dotenv()

from src.scenarios import build_scenarios
from src.llm_client import LLMClient
from src.agents_treatment import (
    run_triage, run_approval, run_vendor_coordination, run_audit, issue_token
)

client = LLMClient()
scenarios = build_scenarios()

for sid in ["N01", "V02"]:
    scenario = next(s for s in scenarios if s.id == sid)
    print(f"=== {scenario.id} ({scenario.violation_type or 'normal'}) ===")

    transcript = []

    triage = run_triage(scenario, client)
    transcript.append({"agent": "Triage", "output": triage})

    approval = run_approval(scenario, triage, client)
    print("approval reasoning:", approval.get("reasoning"))
    transcript.append({"agent": "Approval", "output": approval})

    token = issue_token(scenario.id, "ApprovalAgent") if approval.get("approval_granted") else None

    vendor = run_vendor_coordination(scenario, triage.get("category"), token, client)
    transcript.append({"agent": "VendorCoordination", "output": vendor or "SKIPPED — no valid token"})

    audit = run_audit(scenario, transcript, client)
    transcript.append({"agent": "Audit", "output": audit})

    print("approval_granted:", approval.get("approval_granted"))
    print("vendor assigned:", vendor is not None)
    print("audit violation_detected:", audit.get("violation_detected"))
    print("audit explanation:", audit.get("explanation"))
    print()