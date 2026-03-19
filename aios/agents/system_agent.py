from aios.agents.tool_agent import ToolAgent


class SystemAgent(ToolAgent):

    def __init__(self):

        super().__init__("SystemAgent")

    def execute(self, payload):

        command = payload.get("command")

        result = self.use_tool(
            "system",
            command=command
        )

        self.use_tool(
            "vector_memory",
            action="store",
            text=f"System command: {command} | Result: {result}"
        )

        return result