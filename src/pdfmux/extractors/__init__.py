"""Extractor registry — maps PDF types to extraction strategies."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class Extractor(Protocol):
    """Protocol for PDF extractors."""

    def extract(self, file_path: str | Path, pages: list[int] | None = None) -> str:
        """Extract text from a PDF, returning raw Markdown-ish text."""
        ...

    @property
    def name(self) -> str:
        """Human-pdfmux name of this extractor."""
        ...
