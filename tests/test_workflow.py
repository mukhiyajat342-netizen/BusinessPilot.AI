import unittest

from src.businesspilot.schemas import BusinessType, BusinessProfile, BusinessRequest
from src.businesspilot.state import BusinessState
from src.businesspilot.agents.orchestrator import OrchestratorAgent


class WorkflowTests(unittest.TestCase):
    def make_state(self):
        profile = BusinessProfile(
            name="Test Store",
            business_type=BusinessType.RETAIL,
            description="Small retail store",
        )
        request = BusinessRequest(
            profile=profile,
            problem="Low sales conversion and pricing problems",
            budget=1000,
            goal="Improve conversion and revenue",
            duration_days=10,
        )
        return BusinessState(request=request)

    def test_full_workflow(self):
        state = self.make_state()
        result = OrchestratorAgent().run(state)
        self.assertIn(result["decision"], ("approved", "revision_limit_reached"))
        self.assertGreaterEqual(result["evaluation_score"], 0)
        self.assertLessEqual(result["evaluation_score"], 100)
        self.assertEqual(
            len(state.execution_data["action_steps"]),
            len(state.strategy_data["strategies"]),
        )
        self.assertAlmostEqual(
            state.finance_data["allocated_budget"],
            sum(x["amount"] for x in state.finance_data["allocations"]),
            places=2,
        )

    def test_negative_budget_rejected(self):
        profile = BusinessProfile("Test", BusinessType.OTHER, "Test")
        with self.assertRaises(ValueError):
            BusinessRequest(profile, "Problem", -1, "Goal", 5)


if __name__ == "__main__":
    unittest.main()
