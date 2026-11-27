from src.businesspilot.state import BusinessState


class StrategyAgent:
    def run(self, state: BusinessState):
        print("\n[Strategy Agent] Building initial strategies...")
        opportunities = state.research_data.get("opportunities", [])
        for opportunity in opportunities:
            state.add_strategy(
                opportunity,
                f"Create and test a practical action plan for: {opportunity}",
                "High",
                "Strategy Agent",
            )
        result = {
            "business_name": state.request.profile.name,
            "problem": state.request.problem,
            "strategies": state.strategy_data.get("strategies", []),
        }
        state.add_message("Strategy Agent", "Orchestrator Agent", result)
        state.update_stage("strategy_completed")
        return result
