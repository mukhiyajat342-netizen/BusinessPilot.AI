from src.businesspilot.state import BusinessState


class CustomerSupportAgent:
    def run(self, state: BusinessState):
        problem = state.request.problem.lower()
        if "complaint" in problem:
            recommendations = [
                "Create a consistent process for recording and resolving complaints.",
                "Review recurring complaint themes weekly.",
                "Ask customers whether the resolution addressed their concern.",
            ]
        elif "repeat" in problem or "retention" in problem:
            recommendations = [
                "Collect feedback from existing customers.",
                "Test a simple loyalty or follow-up programme.",
                "Track repeat-customer rate over time.",
            ]
        else:
            recommendations = [
                "Collect customer feedback through a short, optional survey.",
                "Set a clear response-time target.",
                "Review customer satisfaction trends regularly.",
            ]
        for item in recommendations:
            state.add_strategy(item, item, "Medium", "Customer Support Agent")
        result = {
            "business_name": state.request.profile.name,
            "recommendations": recommendations,
            "note": "Validate recommendations with actual customer feedback.",
        }
        state.strategy_data["customer_support_data"] = result
        state.add_message("Customer Support Agent", "Finance Agent", result)
        state.update_stage("customer_support_completed")
        return result
