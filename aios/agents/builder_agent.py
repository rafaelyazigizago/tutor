from aios.agents.base_agent import BaseAgent
from aios.agents.agent_generator import AutoAgentBuilder


class BuilderAgent(BaseAgent):

    def __init__(self):

        super().__init__(name="builder")

        self.generator = AutoAgentBuilder()

    def execute(self, payload):

        request = payload.get("request")

        if not request:

            return "BuilderAgent: nenhuma solicitação recebida."

        agent_name = payload.get("agent_name", "generated_agent")

        print("\n🔧 BuilderAgent criando novo agente...")

        code = self.generator.generate_agent_code(
            agent_name,
            request
        )

        file_path = self.generator.create_agent_file(
            agent_name,
            code
        )

        print(f"\n✅ Novo agente criado em: {file_path}")

        return file_path