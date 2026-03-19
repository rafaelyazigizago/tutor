from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any
from rich import print


class BaseAgent(ABC):

    def __init__(self, name: str):

        self.name = name
        self.created_at = datetime.utcnow()

    def run(self, payload: Dict[str, Any]):

        print(f"[cyan]Agent starting:[/cyan] {self.name}")

        try:

            result = self.execute(payload)

            print(f"[green]Agent finished:[/green] {self.name}")

            return result

        except Exception as e:

            print(f"[red]Agent error:[/red] {self.name} -> {e}")

            raise

    @abstractmethod
    def execute(self, payload: Dict[str, Any]):

        pass