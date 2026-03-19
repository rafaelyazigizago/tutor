from .tool import Tool
from aios.memory.vector_memory import VectorMemory


class VectorMemoryTool(Tool):

    def __init__(self):

        super().__init__("vector_memory")

        self.memory = VectorMemory()

    def execute(self, action: str, text: str = "", query: str = ""):

        if action == "store":

            self.memory.store(text)

            return "stored"

        if action == "search":

            return self.memory.search(query)

        raise Exception("Invalid action")