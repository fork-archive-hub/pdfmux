"""LLM provider abstraction — BYOK multi-provider support.

Each provider wraps a single LLM API for vision-based PDF page extraction.
Users bring their own API key; pdfmux auto-detects which provider to use.

Provider priority (when auto-detecting):
  1. Gemini (GEMINI_API_KEY / GOOGLE_API_KEY)
  2. Claude (ANTHROPIC_API_KEY)
  3. OpenAI (OPENAI_API_KEY)
  4. Ollama (OLLAMA_BASE_URL, local)
"""

from __future__ import annotations

import base64
import logging
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

PROVIDERS: list[type[LLMProvider]] = []


class LLMProvider(ABC):
    """Base class for LLM vision providers."""

    name: str
    default_model: str

    @abstractmethod
    def available(self) -> bool:
        """True if SDK installed AND credentials configured."""
        ...

    @abstractmethod
    def extract_page(self, image_bytes: bytes, prompt: str, model: str | None = None) -> str:
        """Send a page image to the LLM and return extracted text."""
        ...

    def sdk_installed(self) -> bool:
        """True if the provider's SDK is importable."""
        return False

    def has_credentials(self) -> bool:
        """True if the provider's API key / endpoint is configured."""
        return False


# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------


class GeminiProvider(LLMProvider):
    name = "gemini"
    default_model = "gemini-2.5-flash"

    def sdk_installed(self) -> bool:
        try:
            import google.genai  # noqa: F401

            return True
        except ImportError:
            return False

    def has_credentials(self) -> bool:
        return bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))

    def available(self) -> bool:
        return self.sdk_installed() and self.has_credentials()

    def extract_page(self, image_bytes: bytes, prompt: str, model: str | None = None) -> str:
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key)
        image_b64 = base64.b64encode(image_bytes).decode()

        response = client.models.generate_content(
            model=model or self.default_model,
            contents=[
                {
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": "image/png", "data": image_b64}},
                    ]
                }
            ],
        )
        return response.text or ""


# ---------------------------------------------------------------------------
# Claude (Anthropic)
# ---------------------------------------------------------------------------


class ClaudeProvider(LLMProvider):
    name = "claude"
    default_model = "claude-sonnet-4-6-20250514"

    def sdk_installed(self) -> bool:
        try:
            import anthropic  # noqa: F401

            return True
        except ImportError:
            return False

    def has_credentials(self) -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    def available(self) -> bool:
        return self.sdk_installed() and self.has_credentials()

    def extract_page(self, image_bytes: bytes, prompt: str, model: str | None = None) -> str:
        import anthropic

        client = anthropic.Anthropic()
        image_b64 = base64.b64encode(image_bytes).decode()

        response = client.messages.create(
            model=model or self.default_model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return response.content[0].text if response.content else ""


# ---------------------------------------------------------------------------
# OpenAI (GPT-4o)
# ---------------------------------------------------------------------------


class OpenAIProvider(LLMProvider):
    name = "openai"
    default_model = "gpt-4o"

    def sdk_installed(self) -> bool:
        try:
            import openai  # noqa: F401

            return True
        except ImportError:
            return False

    def has_credentials(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    def available(self) -> bool:
        return self.sdk_installed() and self.has_credentials()

    def extract_page(self, image_bytes: bytes, prompt: str, model: str | None = None) -> str:
        import openai

        client = openai.OpenAI()
        image_b64 = base64.b64encode(image_bytes).decode()

        response = client.chat.completions.create(
            model=model or self.default_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}",
                                "detail": "high",
                            },
                        },
                    ],
                }
            ],
            max_tokens=4096,
        )
        return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Ollama (local)
# ---------------------------------------------------------------------------


class OllamaProvider(LLMProvider):
    name = "ollama"
    default_model = ""  # must be set via PDFMUX_LLM_MODEL

    def sdk_installed(self) -> bool:
        try:
            import ollama  # noqa: F401

            return True
        except ImportError:
            return False

    def has_credentials(self) -> bool:
        return bool(self._get_model())

    def available(self) -> bool:
        return self.sdk_installed() and self.has_credentials()

    def _get_model(self) -> str:
        return os.environ.get("PDFMUX_LLM_MODEL", "")

    def extract_page(self, image_bytes: bytes, prompt: str, model: str | None = None) -> str:
        import ollama

        use_model = model or self._get_model()
        if not use_model:
            raise ValueError(
                "Ollama requires PDFMUX_LLM_MODEL to be set (e.g. 'llava', 'bakllava')"
            )

        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        client = ollama.Client(host=base_url)
        image_b64 = base64.b64encode(image_bytes).decode()

        response = client.chat(
            model=use_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_b64],
                }
            ],
        )
        return response.message.content or ""


# ---------------------------------------------------------------------------
# Provider registry & resolution
# ---------------------------------------------------------------------------

PROVIDERS = [GeminiProvider, ClaudeProvider, OpenAIProvider, OllamaProvider]


def resolve_provider(
    provider_name: str | None = None, model: str | None = None
) -> LLMProvider:
    """Resolve which LLM provider to use.

    Priority:
      1. Explicit PDFMUX_LLM_PROVIDER env var or provider_name arg
      2. Auto-detect from available API keys (Gemini > Claude > OpenAI > Ollama)

    Raises:
        ValueError: If no provider is available.
    """
    name = provider_name or os.environ.get("PDFMUX_LLM_PROVIDER")

    if name:
        name = name.lower().strip()
        for cls in PROVIDERS:
            if cls.name == name:
                provider = cls()
                if not provider.sdk_installed():
                    raise ValueError(
                        f"Provider '{name}' selected but SDK not installed. "
                        f"Install with: pip install pdfmux[llm-{name}]"
                    )
                return provider
        valid = ", ".join(cls.name for cls in PROVIDERS)
        raise ValueError(f"Unknown LLM provider '{name}'. Valid providers: {valid}")

    # Auto-detect from available credentials
    for cls in PROVIDERS:
        provider = cls()
        if provider.available():
            logger.info("Auto-detected LLM provider: %s", provider.name)
            return provider

    raise ValueError(
        "No LLM provider available. Set one of: "
        "GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY, "
        "or OLLAMA_BASE_URL + PDFMUX_LLM_MODEL"
    )


def available_providers() -> list[LLMProvider]:
    """Return all providers that have SDK installed and credentials configured."""
    return [cls() for cls in PROVIDERS if cls().available()]


def all_provider_status() -> list[dict[str, str | bool]]:
    """Return status of all providers for doctor command."""
    result = []
    for cls in PROVIDERS:
        p = cls()
        result.append(
            {
                "name": p.name,
                "sdk_installed": p.sdk_installed(),
                "has_credentials": p.has_credentials(),
                "available": p.available(),
                "default_model": p.default_model or "(requires PDFMUX_LLM_MODEL)",
            }
        )
    return result
