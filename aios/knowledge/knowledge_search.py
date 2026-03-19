"""
Knowledge Search
Tutor AIOS — Knowledge Layer

Responsável por:
- buscar chunks relevantes no VectorMemory
- retornar contexto para o LLM
"""

from aios.memory.vector_memory import VectorMemory


class KnowledgeSearch:

    def __init__(self):
        self.vector_memory = VectorMemory()

    def search(self, query: str, limit: int = 5):

        results = self.vector_memory.search(
            query,
            limit
        )

        return results

    def build_context(self, query: str, limit: int = 5):

        results = self.search(query, limit)

        context = "\n\n".join(results)

        return context