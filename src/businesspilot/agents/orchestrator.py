from src.businesspilot.state import BusinessState
from src.businesspilot.agents.research import ResearchAgent
from src.businesspilot.agents.strategy import StrategyAgent
from src.businesspilot.agents.finance import FinanceAgent
from src.businesspilot.agents.execution import ExecutionAgent
from src.businesspilot.agents.evaluation import EvaluationAgent
from src.businesspilot.agents.agent_selector import AgentSelector
from src.businesspilot.agents.marketing import MarketingAgent
from src.businesspilot.agents.customer_support import CustomerSupportAgent
from src.businesspilot.agents.operations import OperationsAgent
from src.businesspilot.agents.sales import SalesAgent


class OrchestratorAgent:
    SPECIALISTS = {
        "MarketingAgent": MarketingAgent,
        "CustomerSupportAgent": CustomerSupportAgent,
        "OperationsAgent": OperationsAgent,
        "SalesAgent": SalesAgent,
    }

    def run(self, state: BusinessState):
        print("\n========== BUSINESSPILOT ORCHESTRATOR ==========")
        state.revision_count = 0
        state.evaluation_feedback.clear()

        ResearchAgent().run(state)
        StrategyAgent().run(state)

        selected = AgentSelector().select_specialists(state)
        print("\n[Orchestrator] Selected specialists:", selected)
        for name in selected:
            self.SPECIALISTS[name]().run(state)

        FinanceAgent().run(state)
        ExecutionAgent().run(state)
        evaluation = EvaluationAgent().run(state)

        max_revisions = 2
        while not evaluation["is_approved"] and state.revision_count < max_revisions:
            state.revision_count += 1
            print(f"\n[Orchestrator] Improvement attempt {state.revision_count}/{max_revisions}")
            feedback = evaluation["feedback"]

            budget_issue = any(
                phrase in item.lower()
                for item in feedback
                for phrase in ("budget", "allocation")
            )
            if budget_issue:
                FinanceAgent().run(state)

            ExecutionAgent().run(state, revision_feedback=feedback)
            evaluation = EvaluationAgent().run(state)

        decision = "approved" if evaluation["is_approved"] else "revision_limit_reached"
        state.update_stage("workflow_approved" if evaluation["is_approved"] else "revision_limit_reached")

        result = {
            "business_name": state.request.profile.name,
            "evaluation_score": evaluation["score"],
            "decision": decision,
            "evaluation_feedback": evaluation["feedback"],
            "revision_attempts": state.revision_count,
            "selected_specialists": selected,
            "total_agents_executed": 5 + len(selected),
        }
        print("\n========== ORCHESTRATOR COMPLETED ==========")
        return result
