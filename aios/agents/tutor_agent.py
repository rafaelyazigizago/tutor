"""
Tutor Agent
Tutor AIOS

Agente responsável por ensinar o usuário.
Integrado com KnowledgeSearch (RAG).
"""

from aios.agents.llm_agent import LLMAgent
from aios.knowledge.knowledge_search import KnowledgeSearch
from aios.llm.llm_client import LLMClient


class TutorAgent(LLMAgent):

    def __init__(self):

        super().__init__()

        self.knowledge = KnowledgeSearch()
        self.llm = LLMClient()

    def execute(self, task):

        question = task.payload.get("question", "")

        # buscar contexto relevante
        context = self.knowledge.build_context(question, 5)

        prompt = f"""
Você é um tutor especialista.

Responda a pergunta do aluno usando o contexto fornecido.

CONTEXTO:
{context}

PERGUNTA:
{question}

Resposta:
"""

        answer = self.llm.generate(prompt)

        return {
            "answer": answer
        }