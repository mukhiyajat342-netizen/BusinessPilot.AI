import json
from datetime import datetime

import streamlit as st

from src.businesspilot.schemas import BusinessType, BusinessProfile, BusinessRequest
from src.businesspilot.state import BusinessState
from src.businesspilot.agents.orchestrator import OrchestratorAgent


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="BusinessPilot AI | Business Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# DESIGN SYSTEM
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --bp-bg: #0b1020;
        --bp-panel: #111a2e;
        --bp-panel-2: #151f36;
        --bp-border: rgba(148, 163, 184, .16);
        --bp-text: #edf2ff;
        --bp-muted: #94a3b8;
        --bp-purple: #9b8cff;
        --bp-cyan: #67e8f9;
        --bp-green: #6ee7b7;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(91, 76, 190, .18), transparent 34%),
            radial-gradient(ellipse at 92% 8%, rgba(20, 184, 166, .10), transparent 28%),
            var(--bp-bg);
        color: var(--bp-text);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] { background: rgba(11, 16, 32, .75); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10182b 0%, #0d1425 100%);
        border-right: 1px solid var(--bp-border);
    }
    [data-testid="stSidebar"] > div { padding-top: 1.5rem; }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--bp-text) !important;
        letter-spacing: -.025em;
    }
    p, label, li, [data-testid="stMarkdownContainer"] {
        color: #d7def0;
    }
    .muted { color: var(--bp-muted); }
    .brand-kicker {
        color: var(--bp-cyan);
        text-transform: uppercase;
        letter-spacing: .16em;
        font-size: .72rem;
        font-weight: 700;
        margin-bottom: .45rem;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2rem, 4vw, 3.25rem);
        line-height: 1.05;
        font-weight: 700;
        color: #f8faff;
        margin: 0;
    }
    .hero-subtitle {
        color: #aab7d0;
        font-size: 1.02rem;
        max-width: 720px;
        margin-top: .8rem;
        line-height: 1.65;
    }
    .hero {
        padding: 1.8rem 0 1.2rem 0;
    }
    .panel {
        background: linear-gradient(145deg, rgba(21, 31, 54, .96), rgba(15, 24, 43, .96));
        border: 1px solid var(--bp-border);
        border-radius: 18px;
        padding: 1.15rem 1.25rem;
        margin-bottom: .85rem;
        box-shadow: 0 12px 34px rgba(0,0,0,.12);
    }
    .panel-label {
        color: var(--bp-muted);
        text-transform: uppercase;
        letter-spacing: .1em;
        font-size: .69rem;
        font-weight: 700;
    }
    .panel-value {
        color: #f5f7ff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: .35rem;
    }
    .panel-note { color: var(--bp-muted); font-size: .8rem; margin-top: .2rem; }
    .section-eyebrow {
        color: var(--bp-purple);
        text-transform: uppercase;
        letter-spacing: .13em;
        font-size: .7rem;
        font-weight: 700;
        margin-bottom: .3rem;
    }
    .agent-card {
        background: rgba(21, 31, 54, .82);
        border: 1px solid var(--bp-border);
        border-radius: 14px;
        padding: .9rem 1rem;
        min-height: 100px;
        margin-bottom: .5rem;
    }
    .agent-name { color: #f0f4ff; font-weight: 700; margin-bottom: .25rem; }
    .agent-desc { color: var(--bp-muted); font-size: .82rem; }
    .status-pill {
        display: inline-block;
        border: 1px solid rgba(110,231,183,.25);
        background: rgba(16,185,129,.10);
        color: #86efc5;
        border-radius: 999px;
        padding: .28rem .65rem;
        font-size: .75rem;
        font-weight: 700;
    }
    div.stButton > button, div.stFormSubmitButton > button {
        border-radius: 10px;
        border: 1px solid rgba(167, 139, 250, .45);
        background: linear-gradient(110deg, #7666e8, #5144bd);
        color: white;
        font-weight: 700;
        min-height: 2.8rem;
        transition: .2s ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        border-color: #b9adff;
        background: linear-gradient(110deg, #897bf1, #6255d0);
        color: white;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input {
        background: #0c1528;
        color: #f4f6ff;
        border: 1px solid rgba(148,163,184,.25);
        border-radius: 10px;
    }
    div[data-baseweb="select"] > div {
        background: #0c1528;
        border-color: rgba(148,163,184,.25);
        border-radius: 10px;
    }
    [data-testid="stMetric"] {
        background: rgba(21,31,54,.78);
        border: 1px solid var(--bp-border);
        border-radius: 14px;
        padding: .85rem 1rem;
    }
    [data-testid="stMetricLabel"] { color: #aab7d0; }
    [data-testid="stMetricValue"] { color: #f5f7ff; }
    [data-testid="stTabs"] button {
        color: #aab7d0;
        font-weight: 600;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #c4baff;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--bp-border);
        border-radius: 12px;
        overflow: hidden;
    }
    hr { border-color: var(--bp-border); }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def safe_list(value):
    return value if isinstance(value, list) else []


def build_report(state, result):
    request = state.request
    lines = [
        "# BusinessPilot AI — Business Analysis Report",
        "",
        f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        "",
        "## Business overview",
        f"- Business: {request.profile.name}",
        f"- Type: {request.profile.business_type.value}",
        f"- Description: {request.profile.description}",
        f"- Location: {request.profile.location}",
        f"- Problem: {request.problem}",
        f"- Goal: {request.goal}",
        f"- Planning budget: {money(request.budget)}",
        f"- Duration: {request.duration_days} days",
        "",
        "## Workflow evaluation",
        f"- Score: {result.get('evaluation_score', 'N/A')}/100",
        f"- Decision: {str(result.get('decision', 'N/A')).replace('_', ' ').title()}",
        f"- Revision attempts: {result.get('revision_attempts', 'N/A')}",
        f"- Specialists: {', '.join(result.get('selected_specialists', []))}",
        "",
        "## Action plan",
    ]

    for item in safe_list(state.execution_data.get("action_steps", [])):
        if isinstance(item, dict):
            lines.append(
                f"- {item.get('task_id', item.get('id', 'Task'))}: "
                f"{item.get('task', item.get('description', item))} "
                f"| Days: {item.get('start_day', '?')}–{item.get('end_day', '?')} "
                f"| Budget: {money(item.get('budget', 0))}"
            )
        else:
            lines.append(f"- {item}")

    lines.extend(["", "## Budget allocation"])
    for item in safe_list(state.finance_data.get("allocations", [])):
        if isinstance(item, dict):
            lines.append(f"- {item}")
        else:
            lines.append(f"- {item}")

    lines.extend(["", "## Evaluation feedback"])
    for item in safe_list(result.get("evaluation_feedback", [])):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Prototype notice",
        "Recommendations are rule-based hypotheses. Budget splits are illustrative, "
        "not verified cost estimates. Validate assumptions with real business data "
        "before taking business or financial action.",
    ])
    return "\n".join(lines)


# ------------------------------------------------------------
# SIDEBAR — BUSINESS PROFILE
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧭 BusinessPilot")
    st.caption("AI-powered business planning")
    st.markdown("---")
    st.markdown("### Business profile")

    business_name = st.text_input("Business name", "My Clothing Store")
    business_type = st.selectbox(
        "Business type",
        [item.value for item in BusinessType],
        index=0,
    )
    description = st.text_area(
        "Business description",
        "A small clothing shop",
        height=90,
    )
    location = st.text_input("Location", "Bengaluru")

    st.markdown("---")
    st.markdown("#### How it works")
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-name">01 · Research</div>
            <div class="agent-desc">Understand the business challenge.</div>
        </div>
        <div class="agent-card">
            <div class="agent-name">02 · Strategy</div>
            <div class="agent-desc">Select specialist recommendations.</div>
        </div>
        <div class="agent-card">
            <div class="agent-name">03 · Planning</div>
            <div class="agent-desc">Allocate budget and schedule actions.</div>
        </div>
        <div class="agent-card">
            <div class="agent-name">04 · Evaluation</div>
            <div class="agent-desc">Review and validate the proposed plan.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Prototype · Rule-based recommendations")


# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="brand-kicker">Business intelligence workspace</div>
        <div class="hero-title">Turn business challenges<br>into clear action plans.</div>
        <div class="hero-subtitle">
            Multiple specialist agents work together to understand your business,
            plan the budget, and build a practical roadmap.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<span class="status-pill">● MULTI-AGENT WORKFLOW</span>',
    unsafe_allow_html=True,
)
st.write("")


# ------------------------------------------------------------
# INPUT FORM
# ------------------------------------------------------------
st.markdown('<div class="section-eyebrow">Start a new analysis</div>', unsafe_allow_html=True)
st.subheader("What does your business need help with?")

with st.form("business_request", clear_on_submit=False):
    problem = st.text_area(
        "Describe your business challenge",
        "Low sales conversion and pricing problems",
        height=105,
        placeholder="Example: Customers visit my store but fewer of them complete a purchase.",
    )
    goal = st.text_input(
        "What outcome do you want?",
        "Improve revenue and conversion",
    )

    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input(
            "Planning budget (₹)",
            min_value=0.0,
            value=10000.0,
            step=500.0,
        )
    with col2:
        duration = st.number_input(
            "Plan duration (days)",
            min_value=1,
            max_value=365,
            value=30,
        )

    submitted = st.form_submit_button(
        "✦ Generate business plan",
        type="primary",
        width="stretch",
    )


# ------------------------------------------------------------
# RUN EXISTING BACKEND — PRESERVED
# ------------------------------------------------------------
if submitted:
    if not business_name.strip() or not problem.strip() or not goal.strip():
        st.error("Please complete business name, challenge, and goal.")
    else:
        try:
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

            with st.spinner("Coordinating research, strategy, finance and evaluation agents..."):
                result = OrchestratorAgent().run(state)

            st.session_state["businesspilot_state"] = state
            st.session_state["businesspilot_result"] = result
            st.success("Business analysis completed.")
        except Exception as exc:
            st.error(f"Could not generate the business plan: {exc}")
            st.exception(exc)


# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------
if "businesspilot_result" in st.session_state:
    state = st.session_state["businesspilot_state"]
    result = st.session_state["businesspilot_result"]

    st.markdown("---")
    st.markdown('<div class="section-eyebrow">Analysis complete</div>', unsafe_allow_html=True)
    st.subheader("Your business command centre")

    score = result.get("evaluation_score", 0)
    specialists = result.get("selected_specialists", [])
    decision = str(result.get("decision", "pending")).replace("_", " ").title()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Evaluation score", f"{score}/100")
    with k2:
        st.metric("Specialists selected", len(specialists))
    with k3:
        st.metric("Revision attempts", result.get("revision_attempts", 0))
    with k4:
        st.metric("Agent messages", len(state.messages))

    st.markdown(
        f'<div class="panel"><div class="panel-label">Workflow decision</div>'
        f'<div class="panel-value">{decision}</div>'
        f'<div class="panel-note">Selected specialists: '
        f'{", ".join(specialists) if specialists else "None"}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### Specialist team")
    agent_cols = st.columns(4)
    agent_names = ["Research", "Strategy", "Finance", "Evaluation"]
    agent_descriptions = [
        "Analyses the supplied business context",
        "Builds recommendations and selects specialists",
        "Plans the illustrative budget",
        "Checks the plan and provides feedback",
    ]
    for index, col in enumerate(agent_cols):
        with col:
            st.markdown(
                f'<div class="agent-card"><div class="agent-name">'
                f'{agent_names[index]} Agent</div><div class="agent-desc">'
                f'{agent_descriptions[index]}</div></div>',
                unsafe_allow_html=True,
            )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🗺️ Action plan", "💰 Budget", "🧠 Specialist insights", "📋 Evaluation & messages"]
    )

    with tab1:
        st.markdown("### Execution roadmap")
        st.caption("Tasks and timelines generated by the execution agent.")
        action_steps = safe_list(state.execution_data.get("action_steps", []))
        if action_steps:
            st.dataframe(action_steps, width="stretch", hide_index=True)
        else:
            st.info("No action steps were returned by the execution agent.")

    with tab2:
        st.markdown("### Budget overview")
        total = state.finance_data.get("total_budget", 0)
        allocated = state.finance_data.get("allocated_budget", 0)
        remaining = state.finance_data.get("remaining_budget", 0)

        b1, b2, b3 = st.columns(3)
        b1.metric("Total budget", money(total))
        b2.metric("Allocated", money(allocated))
        b3.metric("Remaining", money(remaining))

        try:
            total_number = float(total or 0)
            allocated_number = float(allocated or 0)
            if total_number > 0:
                st.progress(min(max(allocated_number / total_number, 0.0), 1.0))
                st.caption(f"{allocated_number / total_number:.0%} of the planning budget allocated")
        except (TypeError, ValueError):
            pass

        allocations = safe_list(state.finance_data.get("allocations", []))
        if allocations:
            st.dataframe(allocations, width="stretch", hide_index=True)
        else:
            st.info("No budget allocations were returned.")
        st.caption("Illustrative allocation only. Verify actual costs before spending.")

    with tab3:
        st.markdown("### Recommendations by specialist")
        specialist_data = [
            ("marketing_data", "📣 Marketing"),
            ("customer_support_data", "🤝 Customer support"),
            ("operations_data", "⚙️ Operations"),
            ("sales_data", "📈 Sales"),
        ]
        found_insight = False
        for key, title in specialist_data:
            data = state.strategy_data.get(key)
            if data:
                found_insight = True
                with st.expander(title, expanded=True):
                    recommendations = data.get(
                        "recommendations",
                        [data.get("recommendation", "")],
                    )
                    for recommendation in recommendations:
                        if recommendation:
                            st.markdown(f"- {recommendation}")
        if not found_insight:
            st.info("No specialist recommendations were returned.")

    with tab4:
        st.markdown("### Evaluation feedback")
        for item in safe_list(result.get("evaluation_feedback", [])):
            st.markdown(f"- {item}")

        st.markdown("### Communication activity")
        st.metric("Agent-to-agent messages recorded", len(state.messages))
        with st.expander("View communication log"):
            st.json(state.messages)

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------
    st.markdown("---")
    st.markdown('<div class="section-eyebrow">Take your plan with you</div>', unsafe_allow_html=True)
    st.subheader("Export business report")

    report = build_report(state, result)
    export_col1, export_col2 = st.columns([1, 2])
    with export_col1:
        st.download_button(
            "⬇ Download report (.md)",
            data=report,
            file_name="businesspilot_report.md",
            mime="text/markdown",
            width="stretch",
        )
    with export_col2:
        st.caption("The report includes the business overview, evaluation, action plan, budget allocation and prototype notice.")

else:
    st.markdown("---")
    st.markdown(
        """
        <div class="panel">
            <div class="section-eyebrow">Ready when you are</div>
            <h3 style="margin-top:.35rem">Your next business decision starts here.</h3>
            <p class="muted">
                Enter your business challenge above and generate a coordinated plan
                from the specialist-agent workflow.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "BusinessPilot AI · Prototype build · Recommendations are rule-based hypotheses, "
    "not verified live market research or professional financial advice."
)
