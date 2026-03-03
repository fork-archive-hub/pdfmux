"""Table extractor — Docling for PDFs with complex tables.

Deferred to v0.2.0. This is a placeholder that will use Docling
for 97.9% table accuracy.
"""

from __future__ import annotations

from pathlib import Path


class TableExtractor:
    """Extract tables from PDFs using Docling (v0.2.0)."""

    @property
    def name(self) -> str:
        return "docling (tables)"

    def extract(self, file_path: str | Path, pages: list[int] | None = None) -> str:
        raise NotImplementedError(
            "Table extraction via Docling is planned for v0.2.0. "
            "Install with: pip install readable[tables]"
        )
