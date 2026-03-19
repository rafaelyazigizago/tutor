import json
import os
from datetime import datetime


class ExecutionMemory:
    """
    Armazena histórico de execuções do AIOS.
    """

    def __init__(self):

        self.file_path = "data/executions.json"

        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def load(self):

        with open(self.file_path, "r") as f:
            return json.load(f)

    def save(self, record):

        data = self.load()

        data.append(record)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def record_execution(self, objective, plan, tasks_executed, status):

        record = {
            "objective": objective,
            "plan": plan,
            "tasks_executed": tasks_executed,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.save(record)