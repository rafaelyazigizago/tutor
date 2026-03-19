from aios.tools.llm_tool import LLMTool
from aios.tools.vector_memory_tool import VectorMemoryTool
from aios.tools.planner_tool import PlannerTool
from aios.tools.filesystem_tool import FileSystemTool
from aios.tools.system_tool import SystemTool


class GlobalToolRegistry:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super(GlobalToolRegistry, cls).__new__(cls)

            cls._instance._initialize()

        return cls._instance

    def _initialize(self):

        self.tools = {}

        self.register(LLMTool())
        self.register(VectorMemoryTool())
        self.register(PlannerTool())
        self.register(FileSystemTool())
        self.register(SystemTool())

    def register(self, tool):

        self.tools[tool.name] = tool

    def get(self, name):

        return self.tools.get(name)

    def list(self):

        return list(self.tools.keys())