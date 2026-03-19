from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:

    name: str
    payload: dict

    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"

    def start(self):
        self.status = "running"

    def complete(self):
        self.status = "completed"

    def fail(self):
        self.status = "failed"