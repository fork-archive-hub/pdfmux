"""LLM vision extractor — Gemini Flash for the hardest cases.

Deferred to v0.2.0. This is the premium fallback for handwriting,
complex forms, and other documents that defeat rule-based extraction.
"""

from __future__ import annotations

from pathlib import Path


class LLMExtractor:
    """Extract text from PDFs using LLM vision API (v0.2.0)."""

    @property
    def name(self) -> str:
        return "gemini-flash (LLM)"

    def extract(self, file_path: str | Path, pages: list[int] | None = None) -> str:
        raise NotImplementedError(
            "LLM vision extraction is planned for v0.2.0. "
            "Install with: pip install readable[llm]"
        )
