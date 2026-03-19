from aios.tools.global_registry import GlobalToolRegistry


class AutoAgentBuilder:
    """
    Responsável por gerar novos agentes automaticamente.
    CORREÇÃO: prompt melhorado para evitar async e garantir __init__ correto.
    """

    def __init__(self):

        self.registry = GlobalToolRegistry()

    def clean_code(self, code: str):
        """
        Remove markdown e textos explicativos gerados pelo LLM.
        Mantém apenas código Python.
        """

        if "```" in code:
            code = code.replace("```python", "")
            code = code.replace("```", "")

        lines = code.split("\n")
        cleaned = []

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("Este código"):
                continue
            if stripped.startswith("This code"):
                continue

            cleaned.append(line)

        return "\n".join(cleaned).strip()

    def generate_agent_code(self, agent_name: str, purpose: str):

        prompt = f"""
Você é um engenheiro especialista em sistemas multi-agentes Python.

Crie um agente Python COMPLETO e FUNCIONAL.

REGRAS OBRIGATÓRIAS — SIGA EXATAMENTE:

1. Importar BaseAgent usando:
   from aios.agents.base_agent import BaseAgent

2. Criar classe em PascalCase com sufixo Agent.

3. Herdar de BaseAgent.

4. Implementar __init__ assim (OBRIGATÓRIO):
   def __init__(self):
       super().__init__(name="{agent_name}")

5. Implementar execute(self, payload) — NUNCA async.

6. execute() deve retornar um valor (string, dict ou lista).

7. Retornar SOMENTE código Python válido.

8. NÃO usar async def em nenhum método.

9. NÃO escrever explicações ou comentários externos.

10. NÃO usar markdown (sem ```, sem #python).

Nome do agente:
{agent_name}

Objetivo do agente:
{purpose}
"""

        llm = self.registry.get("llm")

        code = llm.execute(prompt=prompt)

        code = self.clean_code(code)

        return code

    def create_agent_file(self, agent_name: str, code: str):

        fs = self.registry.get("filesystem")

        file_path = f"aios/agents/{agent_name}.py"

        fs.execute(
            action="write",
            path=file_path,
            content=code
        )

        return file_path
