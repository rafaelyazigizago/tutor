import requests
from .base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """
    Provider HTTP para Ollama local.
    """

    def __init__(self, model: str, url: str):

        self.model = model
        self.url = f"{url}/api/generate"

    def generate(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:

            response = requests.post(
                self.url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=180
            )

        except requests.exceptions.Timeout:
            return "Ollama error: timeout after 180 seconds. Check if Ollama is running."

        except requests.exceptions.ConnectionError:
            return "Ollama error: cannot connect. Check if Ollama is running at http://localhost:11434"

        if response.status_code != 200:
            return f"Ollama error: {response.text}"

        data = response.json()

        if "response" in data:
            return data["response"]

        return str(data)
