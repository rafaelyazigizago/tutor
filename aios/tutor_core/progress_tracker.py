"""
Progress Tracker
Tutor AIOS - Tutor Core

Responsavel por:
- registrar progresso do aluno por curso
- persistir estado entre sessoes
- consultar historico de aulas
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class ProgressTracker:

    def __init__(self):
        self.data_dir = "data/progress"
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_path(self, course_id: str) -> str:
        return os.path.join(self.data_dir, f"{course_id}.json")

    def _load(self, course_id: str) -> Dict:
        path = self._get_path(course_id)
        if not os.path.exists(path):
            return {
                "course_id": course_id,
                "started_at": datetime.utcnow().isoformat(),
                "last_session": None,
                "completed_modules": [],
                "completed_lessons": [],
                "total_lessons_seen": 0,
                "sessions": []
            }
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, course_id: str, data: Dict):
        path = self._get_path(course_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def record_lesson(self, course_id: str, module: str, lesson_topic: str):
        """
        Registra que o aluno completou uma aula.
        """
        data = self._load(course_id)

        lesson_entry = {
            "module": module,
            "topic": lesson_topic,
            "completed_at": datetime.utcnow().isoformat()
        }

        data["completed_lessons"].append(lesson_entry)
        data["total_lessons_seen"] += 1
        data["last_session"] = datetime.utcnow().isoformat()

        if module not in data["completed_modules"]:
            data["completed_modules"].append(module)

        session = {
            "timestamp": datetime.utcnow().isoformat(),
            "module": module,
            "topic": lesson_topic
        }
        data["sessions"].append(session)

        self._save(course_id, data)

        return lesson_entry

    def get_progress(self, course_id: str) -> Dict:
        """
        Retorna o progresso atual do aluno no curso.
        """
        return self._load(course_id)

    def get_last_topic(self, course_id: str) -> str:
        """
        Retorna o ultimo topico estudado.
        """
        data = self._load(course_id)
        lessons = data.get("completed_lessons", [])
        if not lessons:
            return None
        return lessons[-1]["topic"]

    def summary(self, course_id: str) -> str:
        """
        Retorna um resumo textual do progresso.
        """
        data = self._load(course_id)
        total = data["total_lessons_seen"]
        last = data["last_session"]
        modules = data["completed_modules"]

        if total == 0:
            return f"Curso '{course_id}': nenhuma aula realizada ainda."

        return (
            f"Curso '{course_id}': {total} aula(s) concluida(s). "
            f"Modulos vistos: {', '.join(modules)}. "
            f"Ultima sessao: {last}."
        )
