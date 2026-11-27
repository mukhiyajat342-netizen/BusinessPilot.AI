from src.businesspilot.state import BusinessState


class FinanceAgent:
    """Creates an illustrative allocation; it is not a real cost estimate."""

    def run(self, state: BusinessState):
        print("\n[Finance Agent] Allocating the planning budget...")
        total = round(float(state.request.budget), 2)
        strategies = state.strategy_data.get("strategies", [])
        allocations = []
        count = len(strategies)

        if count:
            base = round(total / count, 2)
            used = 0.0
            for index, task in enumerate(strategies):
                amount = round(total - used, 2) if index == count - 1 else base
                used = round(used + amount, 2)
                allocations.append({
                    "task_id": task["task_id"],
                    "task": task["strategy"],
                    "amount": amount,
                })

        allocated = round(sum(item["amount"] for item in allocations), 2)
        result = {
            "total_budget": total,
            "allocated_budget": allocated,
            "remaining_budget": round(total - allocated, 2),
            "allocations": allocations,
            "assumptions": [
                "Allocations are illustrative and evenly distributed.",
                "Actual supplier quotes, taxes, and operating costs are not included.",
                "Human approval and cost verification are required before spending.",
            ],
        }
        state.finance_data = result
        state.add_message("Finance Agent", "Execution Agent", result)
        state.update_stage("finance_completed")
        return result
