class AgentSelector:
    """Transparent keyword-based routing for the deterministic prototype."""

    RULES = {
        "MarketingAgent": (
            "sales", "marketing", "promotion", "brand", "visibility",
            "growth", "orders", "awareness", "campaign",
        ),
        "CustomerSupportAgent": (
            "complaint", "complaints", "customer service", "satisfaction",
            "customer support", "repeat", "retention", "feedback",
        ),
        "OperationsAgent": (
            "stock", "inventory", "shortage", "delivery", "shipping",
            "delay", "order processing", "operations", "efficiency", "warehouse",
        ),
        "SalesAgent": (
            "conversion", "pricing", "price", "revenue", "closing",
            "upsell", "cross-sell", "average order value", "lead", "leads",
        ),
    }

    def select_specialists(self, state):
        req = state.request
        text = " ".join((
            req.problem, req.goal, req.profile.description,
            req.profile.business_type.value,
        )).lower()
        return [
            agent for agent, keywords in self.RULES.items()
            if any(keyword in text for keyword in keywords)
        ]
