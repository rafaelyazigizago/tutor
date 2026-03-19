"""
Tutor Knowledge Responder
Tutor AIOS — Knowledge Layer

Responsável por:
- buscar conhecimento no VectorMemory
- montar prompt com contexto
- consultar o LLM
"""

from aios.knowledge.knowledge_search import KnowledgeSearch
from aios.llm.llm_client import LLMClient


class TutorKnowledgeResponder:

    def __init__(self):

        self.search = KnowledgeSearch()
        self.llm = LLMClient()

    def answer(self, question: str):

        context = self.search.build_context(question, 5)

        prompt = f"""
Você é um tutor especializado.

Use apenas o contexto abaixo para responder a pergunta.

CONTEXTO:
{context}

PERGUNTA:
{question}

Resposta:
"""

        response = self.llm.generate(prompt)

        return response