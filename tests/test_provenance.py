"""Tests for provenance metadata on chunks."""

from __future__ import annotations

from pathlib import Path

import pdfmux
from pdfmux.chunking import chunk_by_sections


class TestChunkProvenance:
    """Chunks should carry extractor and ocr_applied metadata."""

    def test_chunk_has_extractor_field(self) -> None:
        """Chunk dataclass should have extractor field."""
        text = "# Heading\n\nSome content here that is long enough."
        chunks = chunk_by_sections(text, confidence=0.9, extractor="pymupdf4llm")
        assert len(chunks) > 0
        assert chunks[0].extractor == "pymupdf4llm"

    def test_chunk_has_ocr_applied_field(self) -> None:
        """Chunk dataclass should have ocr_applied field."""
        text = "# Heading\n\nSome OCR content here."
        chunks = chunk_by_sections(text, confidence=0.85, extractor="rapidocr", ocr_applied=True)
        assert len(chunks) > 0
        assert chunks[0].ocr_applied is True

    def test_chunk_defaults(self) -> None:
        """Default extractor and ocr_applied should be empty/False."""
        text = "# Heading\n\nContent."
        chunks = chunk_by_sections(text, confidence=0.9)
        assert len(chunks) > 0
        assert chunks[0].extractor == ""
        assert chunks[0].ocr_applied is False

    def test_llm_format_includes_provenance(self, digital_pdf: Path) -> None:
        """LLM format output should include extractor and ocr_applied per chunk."""
        chunks = pdfmux.load_llm_context(digital_pdf)
        assert len(chunks) > 0
        for chunk in chunks:
            assert "extractor" in chunk
            assert "ocr_applied" in chunk
            assert isinstance(chunk["ocr_applied"], bool)
