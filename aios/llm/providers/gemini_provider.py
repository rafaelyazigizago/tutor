import os
import requests
from aios.llm.providers.base_provider import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """
    Provider para Google Gemini API.
    Usado para: ingestão e processamento de conhecimento.
    Modelo padrão: gemini-2.0-flash
    """

    def __init__(self, model: str = None):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise Exception("GEMINI_API_KEY não encontrada no .env")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def generate(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024
            }
        }
        response = requests.post(self.url, json=payload, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
