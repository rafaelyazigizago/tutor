import os
import requests
from aios.llm.providers.base_provider import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    """
    Provider para Anthropic Claude API.
    Usado para: raciocínio profundo e avaliação pedagógica.
    Modelo padrão: claude-haiku-4-5-20251001
    """

    def __init__(self, model: str = None):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise Exception("ANTHROPIC_API_KEY não encontrada no .env")
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
        self.url = "https://api.anthropic.com/v1/messages"

    def generate(self, prompt: str) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
