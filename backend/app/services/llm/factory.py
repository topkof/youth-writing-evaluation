from typing import Any, Dict, List, Optional, Type
from app.services.llm.base import LLMProvider
from app.services.llm.openai import OpenAIProvider


class LLMFactory:
    _providers: Dict[str, Type[LLMProvider]] = {
        "openai": OpenAIProvider,
    }

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]) -> None:
        cls._providers[name] = provider_class

    @classmethod
    def get_provider(
        cls,
        provider_name: str,
        api_key: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        provider_class = cls._providers.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")
        return provider_class(api_key=api_key, **kwargs)

    @classmethod
    def list_providers(cls) -> List[str]:
        return list(cls._providers.keys())

    @classmethod
    def get_provider_info(cls, provider_name: str) -> Dict[str, Any]:
        provider_class = cls._providers.get(provider_name.lower())
        if not provider_class:
            return {}
        provider = provider_class()
        return {
            "name": provider.provider_name,
            "models": provider.supported_models
        }
