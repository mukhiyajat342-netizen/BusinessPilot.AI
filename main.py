from src.businesspilot.schemas import BusinessType, BusinessProfile, BusinessRequest
from src.businesspilot.state import BusinessState
from src.businesspilot.agents.orchestrator import OrchestratorAgent


def run_demo():
    profile = BusinessProfile(
        name="My Clothing Store",
        business_type=BusinessType.RETAIL,
        description="A small clothing shop",
        location="Bengaluru",
    )
    request = BusinessRequest(
        profile=profile,
        problem="My store has low sales conversion and pricing problems",
        budget=10000,
        goal="Improve revenue and conversion",
        duration_days=30,
    )
    state = BusinessState(request=request)
    result = OrchestratorAgent().run(state)

    print("\n" + "=" * 60)
    print("BUSINESSPILOT AI — BUSINESS ANALYSIS REPORT")
    print("=" * 60)
    print(f"Business: {request.profile.name} ({request.profile.business_type.value})")
    print(f"Problem: {request.problem}")
    print(f"Goal: {request.goal}")
    print(f"Budget: Rs. {request.budget:,.2f}")
    print(f"Duration: {request.duration_days} days")

    print("\nSPECIALISTS")
    for agent in result["selected_specialists"]:
        print("-", agent)
    if not result["selected_specialists"]:
        print("- No specialist selected")

    print("\nBUDGET ALLOCATION (ILLUSTRATIVE)")
    for item in state.finance_data.get("allocations", []):
        print(f"- {item['task_id']} | {item['task']}: Rs. {item['amount']:,.2f}")
    print("Remaining:", f"Rs. {state.finance_data.get('remaining_budget', 0):,.2f}")

    print("\nACTION PLAN")
    for step in state.execution_data.get("action_steps", []):
        print(
            f"- {step['task_id']} {step['task']} | "
            f"{step['timeline']} | Rs. {step['budget']:,.2f}"
        )

    print("\nEVALUATION")
    print("Score:", result["evaluation_score"], "/ 100")
    print("Decision:", result["decision"])
    print("Revision attempts:", result["revision_attempts"])
    for item in result["evaluation_feedback"]:
        print("-", item)

    print("\nCOMMUNICATION")
    print("Agent messages:", len(state.messages))
    print("Final stage:", state.current_stage)
    print("\nNote: This prototype uses rule-based recommendations, not verified live market research.")
    return state, result


if __name__ == "__main__":
    run_demo()
