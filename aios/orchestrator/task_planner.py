import json
import re

from aios.orchestrator.task import Task
from aios.orchestrator.task_types import TaskTypes
from aios.orchestrator.llm_planner import LLMPlanner


class TaskPlanner:
    """
    Converte resposta do LLMPlanner em lista de Tasks.
    CORREÇÃO: parse robusto de JSON via regex — extrai JSON mesmo
    quando o LLM envolve a resposta em markdown ou texto explicativo.
    """

    def __init__(self, router):

        self.router = router
        self.llm_planner = LLMPlanner()

    def create_plan(self, objective: str):

        print("\n🧠 Gerando plano com LLM...")

        response = self.llm_planner.generate_plan(objective)

        steps = self._parse_plan(response, objective)

        # deduplicar por tipo
        seen = set()
        filtered = []

        for step in steps:
            step_type = step.get("type")
            if step_type and step_type not in seen:
                seen.add(step_type)
                filtered.append(step)

        tasks = []

        for step in filtered:
            task = Task(
                name=step["type"],
                payload=step.get("payload", {})
            )
            tasks.append(task)

        print(f"   Plano gerado: {[t.name for t in tasks]}")

        return tasks

    def _parse_plan(self, response: str, objective: str):
        """
        CORREÇÃO: tenta extrair JSON da resposta do LLM de forma robusta.
        O LLM frequentemente retorna JSON dentro de ```json ... ``` ou com
        texto explicativo antes/depois.
        """

        # tentativa 1: parse direto
        try:
            return json.loads(response)
        except Exception:
            pass

        # tentativa 2: extrair array JSON via regex (captura [...])
        match = re.search(r"\[.*?\]", response, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass

        # tentativa 3: extrair objeto JSON individual e envolver em lista
        match = re.search(r"\{.*?\}", response, re.DOTALL)

        if match:
            try:
                return [json.loads(match.group())]
            except Exception:
                pass

        # fallback: plano padrão
        print("⚠️  LLM não retornou JSON válido. Usando plano padrão.")

        return [
            {
                "type": TaskTypes.RESEARCH,
                "payload": {"topic": objective}
            },
            {
                "type": TaskTypes.BUILDER,
                "payload": {"request": f"Criar código relacionado a: {objective}"}
            }
        ]
