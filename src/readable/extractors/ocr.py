"""OCR extractor — for scanned/image-based PDFs.

Deferred to v0.2.0. Will use Surya or PaddleOCR.
"""

from __future__ import annotations

from pathlib import Path


class OCRExtractor:
    """Extract text from scanned PDFs using OCR (v0.2.0)."""

    @property
    def name(self) -> str:
        return "surya (OCR)"

    def extract(self, file_path: str | Path, pages: list[int] | None = None) -> str:
        raise NotImplementedError(
            "OCR extraction is planned for v0.2.0. "
            "Install with: pip install readable[ocr]"
        )
