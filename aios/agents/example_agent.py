from .base_agent import BaseAgent


class ExampleAgent(BaseAgent):

    def __init__(self):

        super().__init__("ExampleAgent")

    def execute(self, payload):

        print("Payload recebido:", payload)

        return {"status": "ok"}