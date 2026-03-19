from aios.agents.base_agent import BaseAgent


class GeneratedAgent(BaseAgent):
    """
    Agente de exemplo gerado automaticamente.
    CORREÇÃO: removido async def — execute() deve ser síncrono.
    """

    def __init__(self):
        super().__init__(name="generated")

    def execute(self, payload):

        print("Agente executado com payload:", payload)

        return {"status": "success", "payload": payload}
