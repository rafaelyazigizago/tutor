import os
import requests
from aios.llm.providers.base_provider import BaseLLMProvider


class GroqProvider(BaseLLMProvider):
    """
    Provider para Groq API (OpenAI-compatible).
    Usado para: conversa em tempo real com o aluno.
    Modelo padrão: llama-3.3-70b-versatile
    """

    def __init__(self, model: str = None):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise Exception("GROQ_API_KEY não encontrada no .env")
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
