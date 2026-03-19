from .tool import Tool
from aios.agents.planner import AgentPlanner


class PlannerTool(Tool):

    def __init__(self):

        super().__init__("planner")

        self.planner = AgentPlanner()

    def execute(self, objective: str):

        plan = self.planner.create_plan(objective)

        return plan