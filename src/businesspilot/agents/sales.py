from src.businesspilot.state import BusinessState


class SalesAgent:
    def run(self, state: BusinessState):
        problem = state.request.problem.lower()
        recommendations = []

        if any(word in problem for word in ("conversion", "lead", "leads")):
            recommendations.extend([
                "Map the steps between customer enquiry and purchase.",
                "Record where potential customers stop progressing.",
            ])
        if any(word in problem for word in ("pricing", "price", "expensive")):
            recommendations.extend([
                "Compare the current offer and pricing with verified alternatives.",
                "Review price against product costs and customer-perceived value.",
            ])
        if any(word in problem for word in ("revenue", "upsell", "cross-sell")):
            recommendations.extend([
                "Identify relevant complementary products or services.",
                "Track average order value and revenue trends.",
            ])
        if not recommendations:
            recommendations = [
                "Track daily sales and best-performing offers.",
                "Review customer purchase patterns.",
            ]

        for item in recommendations:
            state.add_strategy(item, item, "High", "Sales Agent")
        result = {
            "business_name": state.request.profile.name,
            "recommendations": recommendations,
            "note": "Prototype recommendations; sales records are needed for validation.",
        }
        state.strategy_data["sales_data"] = result
        state.add_message("Sales Agent", "Finance Agent", result)
        state.update_stage("sales_completed")
        return result
