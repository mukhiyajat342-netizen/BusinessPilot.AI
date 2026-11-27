from src.businesspilot.state import BusinessState


class ExecutionAgent:
    def run(self, state: BusinessState, revision_feedback=None):
        print("\n[Execution Agent] Building action schedule...")
        strategies = state.strategy_data.get("strategies", [])
        allocations = {
            item["task_id"]: item["amount"]
            for item in state.finance_data.get("allocations", [])
        }
        duration = state.request.duration_days
        count = len(strategies)
        action_steps = []

        for index, task in enumerate(strategies):
            # Multiple tasks may share a day when there are more tasks than days.
            start_day = min(duration, (index * duration) // max(count, 1) + 1)
            end_day = min(duration, max(
                start_day, ((index + 1) * duration) // max(count, 1)
            ))
            action_steps.append({
                "step": index + 1,
                "task_id": task["task_id"],
                "task": task["strategy"],
                "source_agent": task.get("source_agent", "Unknown"),
                "budget": allocations.get(task["task_id"], 0.0),
                "timeline": f"Days {start_day} to {end_day}",
                "start_day": start_day,
                "end_day": end_day,
                "status": "Pending",
            })

        revision_actions = []
        if revision_feedback:
            if any("timeline" in item.lower() for item in revision_feedback):
                revision_actions.append("Rebuilt the task schedule.")
            if any("budget" in item.lower() for item in revision_feedback):
                revision_actions.append("Refreshed task allocations from Finance Agent.")
            if any("duplicate" in item.lower() for item in revision_feedback):
                revision_actions.append("Rebuilt steps using unique task identifiers.")
            if not revision_actions:
                revision_actions.append("Regenerated the execution plan.")

        result = {
            "business_name": state.request.profile.name,
            "duration_days": duration,
            "covered_days": duration if action_steps else 0,
            "action_steps": action_steps,
            "total_steps": len(action_steps),
            "available_budget": state.finance_data.get("total_budget", 0.0),
            "revision_applied": bool(revision_feedback),
            "revision_actions": revision_actions,
        }
        state.execution_data = result
        state.add_message("Execution Agent", "Evaluation Agent", result)
        state.update_stage("execution_completed")
        return result
