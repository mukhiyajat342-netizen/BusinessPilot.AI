from src.businesspilot.state import BusinessState


class ResearchAgent:
    """Creates initial hypotheses; it does not fetch or verify live market data."""

    def run(self, state: BusinessState):
        print("\n[Research Agent] Analysing the supplied business context...")
        req = state.request
        findings = {
            "business_name": req.profile.name,
            "business_type": req.profile.business_type.value,
            "problem": req.problem,
            "goal": req.goal,
            "possible_causes": [
                "The customer journey may contain friction.",
                "The offer, pricing, or product positioning may need review.",
                "The business may need clearer performance tracking.",
            ],
            "opportunities": [
                "Understand customer needs using direct feedback.",
                "Improve the customer journey and communication.",
                "Track a small set of measurable business KPIs.",
            ],
            "data_gaps": [
                "No sales history or conversion data was supplied.",
                "No customer interviews or survey results were supplied.",
                "Competitor pricing has not been independently verified.",
            ],
            "research_type": "Initial hypotheses based only on user-provided information",
        }
        state.research_data = findings
        state.add_message("Research Agent", "Strategy Agent", findings)
        state.update_stage("research_completed")
        print("[Research Agent] Initial analysis completed.")
        return findings
