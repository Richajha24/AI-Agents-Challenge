from app.providers.base import AIProvider
from app.providers.claude import ClaudeProvider
from app.providers.gemini import GeminiProvider
from app.providers.openai import OpenAIProvider


def get_provider(provider_name: str) -> AIProvider:
    providers: dict[str, type[AIProvider]] = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "gemini": GeminiProvider,
    }
    try:
        return providers[provider_name.lower()]()
    except KeyError as exc:
        raise ValueError(f"Unsupported AI provider: {provider_name}") from exc
