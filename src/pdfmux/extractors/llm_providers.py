"""Backward-compatibility shim — imports from pdfmux.providers.

All provider classes and functions have moved to pdfmux.providers/.
This module re-exports everything so existing imports continue to work.
"""

from pdfmux.providers import (  # noqa: F401
    CostEstimate,
    LLMProvider,
    ModelInfo,
    all_provider_status,
    available_providers,
    resolve_provider,
)
from pdfmux.providers.claude import ClaudeProvider  # noqa: F401
from pdfmux.providers.gemini import GeminiProvider  # noqa: F401
from pdfmux.providers.ollama import OllamaProvider  # noqa: F401
from pdfmux.providers.openai_native import OpenAINativeProvider as OpenAIProvider  # noqa: F401

# Keep PROVIDERS list for backward compat
PROVIDERS = [GeminiProvider, ClaudeProvider, OpenAIProvider, OllamaProvider]
