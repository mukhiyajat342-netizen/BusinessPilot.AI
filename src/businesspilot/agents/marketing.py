from src.businesspilot.state import BusinessState


class MarketingAgent:
    def run(self, state: BusinessState):
        kind = state.request.profile.business_type.value
        suggestions = {
            "restaurant": ["Test a local repeat-visit offer with clear terms."],
            "retail": ["Run a small, measurable local product campaign."],
            "ecommerce": ["Improve product discovery and test a focused online campaign."],
            "startup": ["Test one clearly defined customer segment and message."],
            "freelancer": ["Publish a focused portfolio case study and service offer."],
        }
        recommendation = suggestions.get(
            kind, ["Test a focused customer-acquisition message with a small audience."]
        )[0]
        state.add_strategy(recommendation, recommendation, "High", "Marketing Agent")
        result = {
            "business_name": state.request.profile.name,
            "recommendations": [recommendation],
            "note": "Prototype recommendation; validate audience response before spending.",
        }
        state.strategy_data["marketing_data"] = result
        state.add_message("Marketing Agent", "Finance Agent", result)
        state.update_stage("marketing_completed")
        return result
