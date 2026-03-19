import os
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = ROOT / "logs"
BUILD_LOG = LOG_DIR / "build"
COMMAND_LOG = LOG_DIR / "commands"
DECISION_LOG = LOG_DIR / "decisions"

for p in [BUILD_LOG, COMMAND_LOG, DECISION_LOG]:
    p.mkdir(parents=True, exist_ok=True)


class BuildLogger:

    def __init__(self):
        self.session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    def log_step(self, title: str, description: str):

        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "session": self.session_id,
            "title": title,
            "description": description
        }

        file = BUILD_LOG / f"{self.session_id}.log"

        with open(file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log, indent=2))
            f.write("\n")

    def log_command(self, command: str):

        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "session": self.session_id,
            "command": command
        }

        file = COMMAND_LOG / f"{self.session_id}.log"

        with open(file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log))
            f.write("\n")

    def log_decision(self, decision: str):

        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "session": self.session_id,
            "decision": decision
        }

        file = DECISION_LOG / f"{self.session_id}.log"

        with open(file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log))
            f.write("\n")