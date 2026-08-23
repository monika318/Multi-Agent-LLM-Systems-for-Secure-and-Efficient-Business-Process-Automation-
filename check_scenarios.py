from src.scenarios import build_scenarios

scenarios = build_scenarios()
print(f"Total scenarios: {len(scenarios)}")
print(f"Normal: {sum(1 for s in scenarios if not s.injected_violation)}")
print(f"Violation-injected: {sum(1 for s in scenarios if s.injected_violation)}")
print()
for s in scenarios:
    flag = "⚠️ VIOLATION" if s.injected_violation else ""
    print(f"{s.id}  {s.category:12s}  signoff={s.requires_signoff!s:5}  {flag}")