from typing import Any, Dict, List, Optional
from openai import AsyncOpenAI

from app.services.llm.base import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._client: Optional[AsyncOpenAI] = None

    @property
    def provider_name(self) -> str:
        return "OpenAI"

    @property
    def supported_models(self) -> List[str]:
        return ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]

    @property
    def client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.api_key)
        return self._client

    async def generate(
        self,
        prompt: str,
        model: str = "gpt-4-turbo",
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位专业的小学语文教师。"},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )

        return LLMResponse(
            content=response.choices[0].message.content or "",
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            model=model,
            finish_reason=response.choices[0].finish_reason,
            raw_response=response
        )

    def validate_api_key(self, api_key: str) -> bool:
        try:
            client = AsyncOpenAI(api_key=api_key)
            return True
        except Exception:
            return False

    def to_config_dict(self, api_key: str) -> Dict[str, Any]:
        return {
            "provider": "openai",
            "api_key": api_key,
            "models": self.supported_models
        }
