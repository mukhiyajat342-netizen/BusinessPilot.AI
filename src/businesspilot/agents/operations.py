from src.businesspilot.state import BusinessState


class OperationsAgent:
    def run(self, state: BusinessState):
        problem = state.request.problem.lower()
        if any(word in problem for word in ("stock", "inventory", "shortage")):
            recommendations = [
                "Record stock movement consistently.",
                "Identify fast-moving and slow-moving items.",
                "Set review thresholds for items that run low.",
            ]
        elif any(word in problem for word in ("delivery", "shipping", "delay")):
            recommendations = [
                "Record dispatch and delivery dates.",
                "Categorise the common causes of delays.",
                "Review dispatch hand-offs and customer updates.",
            ]
        else:
            recommendations = [
                "Document the current operating workflow.",
                "Identify avoidable repeat work or bottlenecks.",
                "Track one operational KPI each week.",
            ]
        for item in recommendations:
            state.add_strategy(item, item, "Medium", "Operations Agent")
        result = {
            "business_name": state.request.profile.name,
            "recommendations": recommendations,
            "note": "Validate against actual operational records.",
        }
        state.strategy_data["operations_data"] = result
        state.add_message("Operations Agent", "Finance Agent", result)
        state.update_stage("operations_completed")
        return result
