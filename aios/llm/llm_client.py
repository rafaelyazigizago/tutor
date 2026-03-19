import os
from dotenv import load_dotenv
from aios.llm.providers.base_provider import BaseLLMProvider

load_dotenv()

TASK_PROVIDER_MAP = {
    "conversation": "groq",
    "ingestion":    "groq",
    "curriculum":   "groq",
    "reasoning":    "anthropic",
    "default":      "groq",
}

FALLBACK_ORDER = ["groq", "anthropic"]


def _build_provider(name: str) -> BaseLLMProvider:
    if name == "groq":
        from aios.llm.providers.groq_provider import GroqProvider
        return GroqProvider()
    elif name == "anthropic":
        from aios.llm.providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider()
    elif name == "ollama":
        from aios.llm.providers.ollama_provider import OllamaProvider
        model = os.getenv("LLM_MODEL", "qwen2.5:7b")
        url = os.getenv("OLLAMA_URL")
        return OllamaProvider(model=model, url=url)
    else:
        raise Exception(f"Provider desconhecido: {name}")


class LLMClient:
    def __init__(self):
        self._forced_provider = os.getenv("LLM_PROVIDER")

    def generate(self, prompt: str, task: str = "default") -> str:
        if self._forced_provider == "ollama":
            provider = _build_provider("ollama")
            return provider.generate(prompt)

        primary = TASK_PROVIDER_MAP.get(task, TASK_PROVIDER_MAP["default"])
        order = [primary] + [p for p in FALLBACK_ORDER if p != primary]

        last_error = None
        for provider_name in order:
            try:
                provider = _build_provider(provider_name)
                result = provider.generate(prompt)
                if provider_name != primary:
                    print(f"[LLMClient] Fallback: usando {provider_name}")
                return result
            except Exception as e:
                last_error = e
                print(f"[LLMClient] Provider {provider_name} falhou: {e}")
                continue

        raise Exception(f"Todos os providers falharam. Ultimo erro: {last_error}")
