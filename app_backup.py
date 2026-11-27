import streamlit as st

from src.businesspilot.schemas import BusinessType, BusinessProfile, BusinessRequest
from src.businesspilot.state import BusinessState
from src.businesspilot.agents.orchestrator import OrchestratorAgent

st.set_page_config(page_title="BusinessPilot AI", page_icon="🧭", layout="wide")

st.title("🧭 BusinessPilot AI")
st.caption("One business problem. Multiple expert agents. One actionable plan.")
st.info(
    "Prototype notice: recommendations are rule-based hypotheses. "
    "Budget splits are illustrative, not verified cost estimates. "
    "Review all suggestions before taking business or financial action."
)

with st.sidebar:
    st.header("Business profile")
    business_name = st.text_input("Business name", "My Clothing Store")
    business_type = st.selectbox(
        "Business type", [item.value for item in BusinessType], index=0
    )
    description = st.text_area("Business description", "A small clothing shop")
    location = st.text_input("Location (optional)", "Bengaluru")

with st.form("business_request"):
    st.subheader("Tell us the business challenge")
    problem = st.text_area(
        "What problem are you facing?",
        "Low sales conversion and pricing problems",
        height=110,
    )
    goal = st.text_input("What is your goal?", "Improve revenue and conversion")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Available planning budget (Rs.)", min_value=0.0, value=10000.0, step=500.0)
    with col2:
        duration = st.number_input("Planning duration (days)", min_value=1, max_value=365, value=30)
    submitted = st.form_submit_button("Generate business plan", type="primary", use_container_width=True)

if submitted:
    if not business_name.strip() or not problem.strip() or not goal.strip():
        st.error("Please complete business name, problem, and goal.")
    else:
        profile = BusinessProfile(
            name=business_name.strip(),
            business_type=BusinessType(business_type),
            description=description.strip(),
            location=location.strip() or "Not provided",
        )
        request = BusinessRequest(
            profile=profile,
            problem=problem.strip(),
            budget=float(budget),
            goal=goal.strip(),
            duration_days=int(duration),
        )
        state = BusinessState(request=request)
        with st.spinner("Coordinating specialist agents..."):
            result = OrchestratorAgent().run(state)
        st.session_state["businesspilot_state"] = state
        st.session_state["businesspilot_result"] = result

if "businesspilot_result" in st.session_state:
    state = st.session_state["businesspilot_state"]
    result = st.session_state["businesspilot_result"]

    st.divider()
    st.subheader("Workflow result")
    c1, c2, c3 = st.columns(3)
    c1.metric("Evaluation score", f"{result['evaluation_score']}/100")
    c2.metric("Specialists selected", len(result["selected_specialists"]))
    c3.metric("Revision attempts", result["revision_attempts"])
    st.write("**Decision:**", result["decision"].replace("_", " ").title())
    st.write("**Specialists:**", ", ".join(result["selected_specialists"]) or "None")

    tab1, tab2, tab3, tab4 = st.tabs(["Action plan", "Budget", "Specialist insights", "Evaluation & messages"])
    with tab1:
        st.dataframe(state.execution_data.get("action_steps", []), use_container_width=True, hide_index=True)
    with tab2:
        st.metric("Total budget", f"Rs. {state.finance_data.get('total_budget', 0):,.2f}")
        st.metric("Allocated", f"Rs. {state.finance_data.get('allocated_budget', 0):,.2f}")
        st.metric("Remaining", f"Rs. {state.finance_data.get('remaining_budget', 0):,.2f}")
        st.dataframe(state.finance_data.get("allocations", []), use_container_width=True, hide_index=True)
        st.caption("Illustrative allocation only. Verify actual costs before spending.")
    with tab3:
        for key, title in [
            ("marketing_data", "Marketing"),
            ("customer_support_data", "Customer support"),
            ("operations_data", "Operations"),
            ("sales_data", "Sales"),
        ]:
            data = state.strategy_data.get(key)
            if data:
                st.markdown(f"**{title}**")
                for recommendation in data.get("recommendations", [data.get("recommendation", "")]):
                    if recommendation:
                        st.write("•", recommendation)
    with tab4:
        for item in result["evaluation_feedback"]:
            st.write("•", item)
        st.caption(f"Agent-to-agent messages recorded: {len(state.messages)}")
        with st.expander("View communication log"):
            st.json(state.messages)
