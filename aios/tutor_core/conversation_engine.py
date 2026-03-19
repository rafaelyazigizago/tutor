"""
Conversation Engine
Tutor AIOS - Tutor Core
"""

import os
from datetime import datetime
from aios.llm.llm_client import LLMClient
from aios.knowledge.knowledge_search import KnowledgeSearch
from typing import List, Dict


SYSTEM_PROMPT = """Voce e um tutor pessoal ensinando em uma conversa direta.

Regras obrigatorias sem excecao:
- Fale como uma pessoa, nao como um documento
- Respostas curtas: no maximo 4 frases por turno
- PROIBIDO usar asteriscos, hifens de lista, negrito, cabecalhos ou qualquer markdown
- PROIBIDO comecar a resposta com o nome do aluno toda vez
- PROIBIDO fazer listas com bullets ou numeracao
- Use linguagem simples e direta
- Ocasionalmente pergunte se entendeu, mas nao em todo turno
- Se o aluno errar, corrija com gentileza e reexplique
- Avance so quando o aluno demonstrar entendimento
- Se pedir para simplificar, use uma analogia do dia a dia em no maximo 3 frases
"""


class ConversationEngine:

    def __init__(self, student_name: str = "Rafael"):
        self.llm = LLMClient()
        self.search = KnowledgeSearch()
        self.student_name = student_name
        self.history: List[Dict] = []
        self.current_topic = None
        self.turns = 0
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.memory_path = os.path.join(base_dir, "memory", "MEMORY.md")
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)

    def start_topic(self, topic: str) -> str:
        self.current_topic = topic
        self.history = []
        self.turns = 0

        context = self.search.build_context(topic, limit=3)

        prompt = (
            SYSTEM_PROMPT
            + "\n\nCONTEXTO DO MATERIAL:\n" + context
            + "\n\nTOPICO DA AULA: " + topic
            + "\n\nPrimeiro turno. Faca uma introducao curta em 2 ou 3 frases sobre o topico."
            + " Nao explique tudo agora. Apresente a ideia central e termine com uma pergunta"
            + " simples para engajar o aluno. Nao use listas. Nao use markdown."
        )

        response = self.llm.generate(prompt, task="conversation")
        self._add_to_history("tutor", response)
        self.turns += 1
        return response

    def respond(self, student_input: str) -> str:
        self._add_to_history("aluno", student_input)

        context = self.search.build_context(
            self.current_topic + " " + student_input, limit=3
        )

        history_text = self._format_history()
        check_understanding = self.turns % 3 == 0

        extra = ""
        if check_understanding:
            extra = "Neste turno, alem de continuar, pergunte de forma natural e breve se o aluno entendeu."

        prompt = (
            SYSTEM_PROMPT
            + "\n\nCONTEXTO DO MATERIAL:\n" + context
            + "\n\nTOPICO DA AULA: " + self.current_topic
            + "\n\nHISTORICO DA CONVERSA:\n" + history_text
            + "\n\nULTIMA MENSAGEM DO ALUNO: " + student_input
            + "\n\n" + extra
            + "\n\nResponda em no maximo 4 frases. Sem markdown. Sem listas."
        )

        response = self.llm.generate(prompt, task="conversation")
        self._add_to_history("tutor", response)
        self.turns += 1

        if len(self.history) >= 12:
            self.end_session()

        return response

    def simplify(self) -> str:
        prompt = (
            SYSTEM_PROMPT
            + "\n\nTOPICO: " + str(self.current_topic)
            + "\n\nHISTORICO:\n" + self._format_history()
            + "\n\nO aluno pediu para simplificar. Use uma analogia do dia a dia."
            + " No maximo 3 frases. Sem markdown. Sem listas."
        )

        response = self.llm.generate(prompt, task="conversation")
        self._add_to_history("tutor", response)
        self.turns += 1
        return response

    def end_session(self):
        topic = self.current_topic or "Topico desconhecido"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        entry = (
            "\n### Sessao " + timestamp
            + "\nTopico: " + topic
            + "\nTurnos: " + str(self.turns)
            + "\nAluno: " + self.student_name
            + "\n---\n"
        )
        with open(self.memory_path, "a") as f:
            f.write(entry)
        self.history = []

    def _add_to_history(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > 10:
            self.history = self.history[-10:]

    def _format_history(self) -> str:
        lines = []
        for entry in self.history[:-1]:
            role = "Tutor" if entry["role"] == "tutor" else self.student_name
            lines.append(role + ": " + entry["content"])
        return "\n".join(lines)

    def get_history(self) -> List[Dict]:
        return self.history
