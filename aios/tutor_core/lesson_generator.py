"""
Lesson Generator
Tutor AIOS — Tutor Core

Responsável por:
- gerar aulas a partir de tópicos
- utilizar RAG (KnowledgeSearch)
"""

from aios.llm.llm_client import LLMClient
from aios.knowledge.knowledge_search import KnowledgeSearch


class LessonGenerator:

    def __init__(self):

        self.llm = LLMClient()
        self.search = KnowledgeSearch()

    def generate_lesson(self, topic: str):

        # buscar contexto no VectorMemory
        context = self.search.build_context(topic, 5)

        prompt = f"""
Você é um tutor especialista.

Utilize o CONTEXTO abaixo para gerar uma aula.

CONTEXTO:
{context}

TEMA DA AULA:
{topic}

Estruture a resposta em:

1. Explicação didática
2. Exemplo prático
3. Exercício para o aluno
4. Desafio avançado
"""

        lesson = self.llm.generate(prompt)

        return lesson
