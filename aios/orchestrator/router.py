class AgentRouter:
    """
    Responsável por decidir qual agente deve executar uma tarefa.
    """

    def __init__(self):

        self.routes = {}

    def register(self, intent: str, agent_name: str):

        self.routes[intent] = agent_name

    def resolve(self, task_payload: dict):

        # pesquisa técnica
        if "topic" in task_payload:
            return self.routes.get("research")

        # planejamento / ensino
        if "objective" in task_payload:
            return self.routes.get("tutor")

        # geração de código
        if "request" in task_payload:
            return self.routes.get("builder")

        # execução de comandos
        if "command" in task_payload:
            return self.routes.get("system")

        return self.routes.get("default")