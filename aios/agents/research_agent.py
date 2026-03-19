from aios.agents.tool_agent import ToolAgent


class ResearchAgent(ToolAgent):

    def __init__(self):

        super().__init__("ResearchAgent")

    def build_prompt(self, topic: str, context: str):

        return f"""
Você é um especialista em engenharia de software, arquitetura de IA e sistemas multi-agentes.

Sua tarefa é realizar uma pesquisa técnica profunda.

TÓPICO:
{topic}

CONTEXTO RECUPERADO:
{context}

Responda de forma estruturada.

1. VISÃO GERAL
2. COMO FUNCIONA
3. COMPONENTES PRINCIPAIS
4. EXEMPLO PRÁTICO
5. BOAS PRÁTICAS
"""

    def execute(self, payload):

        topic = payload.get("topic")

        memories = self.use_tool(
            "vector_memory",
            action="search",
            query=topic
        )

        context = "\n".join(memories) if memories else ""

        prompt = self.build_prompt(topic, context)

        response = self.use_tool(
            "llm",
            prompt=prompt
        )

        self.use_tool(
            "vector_memory",
            action="store",
            text=f"Tópico: {topic} | Resposta: {response}"
        )

        return response