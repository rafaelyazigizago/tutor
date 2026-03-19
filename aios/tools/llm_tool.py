from .tool import Tool
from aios.llm.llm_client import LLMClient


class LLMTool(Tool):

    def __init__(self):

        super().__init__("llm")

        self.client = LLMClient()

    def execute(self, prompt: str):

        return self.client.generate(prompt)