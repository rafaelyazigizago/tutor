"""
Curriculum Engine
Tutor AIOS — Tutor Core

Responsável por:
- analisar conhecimento ingerido
- identificar tópicos principais
- gerar estrutura de curso
"""

from aios.memory.vector_memory import VectorMemory
from aios.llm.llm_client import LLMClient


class CurriculumEngine:

    def __init__(self):

        self.memory = VectorMemory()
        self.llm = LLMClient()

    def generate_curriculum(self, topic: str):

        # usar menos contexto para evitar timeout
        docs = self.memory.search(topic, limit=5)

        context = "\n\n".join(docs)

        prompt = f"""
Você é um arquiteto educacional.

Analise o conteúdo abaixo e gere a estrutura de um curso.

CONTEXTO:
{context}

TEMA:
{topic}

Responda SOMENTE em JSON no formato:

{{
 "curso": "...",
 "modulos": [
   "...",
   "...",
   "..."
 ]
}}
"""

        response = self.llm.generate(prompt)

        return response