from aios.agents.base_agent import BaseAgent
from aios.tools.global_registry import GlobalToolRegistry


class ToolAgent(BaseAgent):

    def __init__(self, name):

        super().__init__(name)

        self.registry = GlobalToolRegistry()

    def use_tool(self, name, **kwargs):

        tool = self.registry.get(name)

        if not tool:
            raise Exception(f"Tool not found: {name}")

        print(f"Using tool: {name}")

        return tool.execute(**kwargs)