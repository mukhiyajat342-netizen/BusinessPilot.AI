from src.businesspilot.state import BusinessState


class EvaluationAgent:
    def run(self, state: BusinessState):
        print("\n[Evaluation Agent] Validating the plan...")
        finance = state.finance_data
        execution = state.execution_data
        strategies = state.strategy_data.get("strategies", [])
        allocations = finance.get("allocations", [])
        steps = execution.get("action_steps", [])
        feedback = []
        score = 100

        total = round(finance.get("total_budget", 0.0), 2)
        allocated = round(finance.get("allocated_budget", 0.0), 2)
        allocation_sum = round(sum(x.get("amount", 0.0) for x in allocations), 2)
        if allocated > total or allocated < 0:
            feedback.append("Allocated budget is outside the available budget.")
            score -= 30
        if allocation_sum != allocated:
            feedback.append("Finance allocation total does not match allocated budget.")
            score -= 20
        if any(x.get("amount", 0.0) < 0 for x in allocations):
            feedback.append("A task has a negative budget allocation.")
            score -= 15
        if not feedback:
            feedback.append("Budget allocation is within the available limit.")

        if not steps:
            feedback.append("No action steps were generated.")
            score -= 30
        else:
            feedback.append("Action steps are available.")

        expected_ids = {item["task_id"] for item in strategies}
        actual_ids = [item.get("task_id") for item in steps]
        if set(actual_ids) != expected_ids or len(actual_ids) != len(set(actual_ids)):
            feedback.append("Action steps contain missing or duplicate task identifiers.")
            score -= 20

        duration = execution.get("duration_days", 0)
        valid_days = set()
        timeline_valid = True
        for item in steps:
            start = item.get("start_day", 0)
            end = item.get("end_day", 0)
            if not (1 <= start <= end <= duration):
                timeline_valid = False
            else:
                valid_days.update(range(start, end + 1))
        if steps and (not timeline_valid or valid_days != set(range(1, duration + 1))):
            feedback.append("Task timelines do not validly cover the requested duration.")
            score -= 25
        elif steps:
            feedback.append("Task timelines cover the requested duration.")

        step_budget = round(sum(item.get("budget", 0.0) for item in steps), 2)
        if step_budget != allocated:
            feedback.append("Action-step budgets do not match Finance allocations.")
            score -= 15

        if state.research_data.get("data_gaps"):
            feedback.append("Research assumptions require validation with real business data.")
            score -= 5

        score = max(0, min(100, score))
        result = {
            "score": score,
            "is_approved": score >= 80,
            "feedback": feedback,
        }
        state.evaluation_data = result
        state.evaluation_feedback.extend(feedback)
        state.add_message("Evaluation Agent", "Orchestrator Agent", result)
        state.update_stage("evaluation_completed")
        return result
