from aios.agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    """
    Agente de validação gerado automaticamente pelo AIOS.
    CORREÇÃO: removido async def — execute() deve ser síncrono.
    """

    def __init__(self):
        super().__init__(name="validation")

    def execute(self, payload):

        question = payload.get("question")

        if question:
            answer = f"Resposta: {question.replace('?', '')}"
            return {"answer": answer}

        return {"error": "Missing question"}
