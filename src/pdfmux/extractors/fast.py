"""Fast extractor — PyMuPDF/pymupdf4llm for digital PDFs.

This is the primary extractor, handling ~90% of PDFs.
Speed: ~0.01s/page. Cost: $0. Accuracy: 98%+ on digital PDFs.
"""

from __future__ import annotations

import logging
from pathlib import Path

import fitz
import pymupdf4llm

logger = logging.getLogger(__name__)


class FastExtractor:
    """Extract text from digital PDFs using pymupdf4llm."""

    @property
    def name(self) -> str:
        return "pymupdf4llm (fast)"

    def extract(self, file_path: str | Path, pages: list[int] | None = None) -> str:
        """Extract Markdown from a digital PDF.

        Uses pymupdf4llm for Markdown output. Falls back to raw PyMuPDF
        text extraction if pymupdf4llm returns empty (happens with some
        PDF encodings).

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

        # Fallback: pymupdf4llm sometimes returns empty for valid PDFs
        # (e.g. spaced-out text, unusual encodings). Use raw fitz extraction.
        if len(result.strip()) < 50:
            logger.info("pymupdf4llm returned near-empty, falling back to raw fitz")
            result = self._extract_raw(file_path, pages)

        return result

    @staticmethod
    def _extract_raw(file_path: Path, pages: list[int] | None = None) -> str:
        """Fallback: extract plain text via fitz when pymupdf4llm fails."""
        doc = fitz.open(str(file_path))
        page_range = pages if pages is not None else list(range(len(doc)))
        parts: list[str] = []

        for page_num in page_range:
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                parts.append(text)

        doc.close()
        return "\n\n---\n\n".join(parts)
