from aios.memory.execution_memory import ExecutionMemory


class PlannerContext:
    """
    Fornece contexto de execução para o planner.
    """

    def __init__(self):

        self.execution_memory = ExecutionMemory()

    def get_recent_executions(self, limit=5):

        data = self.execution_memory.load()

        if not data:
            return []

        return data[-limit:]