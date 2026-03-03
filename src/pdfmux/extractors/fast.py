"""Fast extractor — PyMuPDF/pymupdf4llm for digital PDFs.

This is the primary extractor, handling ~90% of PDFs.
Speed: ~0.01s/page. Cost: $0. Accuracy: 98%+ on digital PDFs.
"""

from __future__ import annotations

from pathlib import Path

import pymupdf4llm


class FastExtractor:
    """Extract text from digital PDFs using pymupdf4llm."""

    @property
    def name(self) -> str:
        return "pymupdf4llm (fast)"

    def extract(self, file_path: str | Path, pages: list[int] | None = None) -> str:
        """Extract Markdown from a digital PDF.

        Args:
            file_path: Path to the PDF file.
            pages: Optional list of 0-indexed page numbers to extract.
                   If None, extracts all pages.

        Returns:
            Markdown text extracted from the PDF.
        """
        file_path = Path(file_path)

        kwargs: dict = {}
        if pages is not None:
            kwargs["pages"] = pages

        result = pymupdf4llm.to_markdown(str(file_path), **kwargs)
        return result
