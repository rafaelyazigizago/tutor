import json
from aios.tools.global_registry import GlobalToolRegistry
from aios.orchestrator.planner_context import PlannerContext


class LLMPlanner:
    """
    Usa LLM para gerar planos dinâmicos de execução
    considerando histórico de execuções.
    """

    def __init__(self):

        self.registry = GlobalToolRegistry()
        self.context = PlannerContext()

    def generate_plan(self, objective: str):

        history = self.context.get_recent_executions()

        prompt = f"""
Você é um planejador de sistemas de agentes de IA.

Use o histórico de execuções passadas para gerar um plano eficiente.

Histórico recente de execuções:
{json.dumps(history, indent=2)}

Tipos de tarefas disponíveis:

research
builder
system

Retorne apenas uma lista JSON.

Exemplo:

[
  {{"type": "research", "payload": {{"topic": "..."}}}},
  {{"type": "builder", "payload": {{"request": "..."}}}}
]

Objetivo:
{objective}
"""

        llm = self.registry.get("llm")

        response = llm.execute(prompt=prompt)

        return response