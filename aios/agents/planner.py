from aios.llm.llm_client import LLMClient


class AgentPlanner:

    def __init__(self):

        self.llm = LLMClient()

    def create_plan(self, objective: str):

        prompt = f"""
Você é um planejador de sistemas de agentes de IA.

Seu trabalho é transformar objetivos em planos práticos
para construir sistemas de agentes e AIOS.

Objetivo:
{objective}

Crie um plano de aprendizado focado em:

- criação de agentes
- arquitetura de AIOS
- orquestração de agentes
- ferramentas de agentes
- memória de agentes

Retorne um plano numerado.
"""

        plan = self.llm.generate(prompt)

        return plan