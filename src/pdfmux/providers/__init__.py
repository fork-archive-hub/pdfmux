"""Provider registry — discover and manage LLM providers.

Built-in providers: Gemini, Claude, OpenAI (GPT-4o), Ollama.
Custom providers via ~/.pdfmux/providers.yaml or entry_points.

Usage:
    from pdfmux.providers import resolve_provider, available_providers

    provider = resolve_provider()  # auto-detect from API keys
    text = provider.extract_page(image_bytes, prompt)
"""

from pdfmux.providers._discovery import (
    all_provider_status,
    available_providers,
    discover_all_providers,
    resolve_provider,
)
from pdfmux.providers.base import CostEstimate, LLMProvider, ModelInfo

__all__ = [
    "LLMProvider",
    "ModelInfo",
    "CostEstimate",
    "resolve_provider",
    "available_providers",
    "all_provider_status",
    "discover_all_providers",
]
