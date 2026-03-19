import os
import requests
from aios.llm.providers.base_provider import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """
    Provider para OpenAI API.
    Usado para: geração de currículo e estruturação de conteúdo.
    Modelo padrão: gpt-4o-mini
    """

    def __init__(self, model: str = None):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise Exception("OPENAI_API_KEY não encontrada no .env")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.url = "https://api.openai.com/v1/chat/completions"

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
