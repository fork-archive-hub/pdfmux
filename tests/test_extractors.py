"""Tests for extractors."""

from __future__ import annotations

from pathlib import Path

import pytest

from readable.extractors.fast import FastExtractor
from readable.extractors.llm import LLMExtractor
from readable.extractors.ocr import OCRExtractor
from readable.extractors.tables import TableExtractor


class TestFastExtractor:
    """Tests for the PyMuPDF fast extractor."""

    def test_extract_digital_pdf(self, digital_pdf: Path) -> None:
        """Should extract text from a digital PDF."""
        ext = FastExtractor()
        text = ext.extract(digital_pdf)
        assert text
        assert len(text) > 50

    def test_extract_empty_pdf(self, empty_pdf: Path) -> None:
        """Should handle empty PDFs gracefully."""
        ext = FastExtractor()
        text = ext.extract(empty_pdf)
        # Empty PDF should return empty or minimal text
        assert isinstance(text, str)

    def test_extractor_name(self) -> None:
        """Should have a descriptive name."""
        ext = FastExtractor()
        assert ext.name == "pymupdf4llm (fast)"


class TestTableExtractor:
    """Tests for the table extractor (v0.2.0 placeholder)."""

    def test_not_implemented(self, digital_pdf: Path) -> None:
        """Should raise NotImplementedError."""
        ext = TableExtractor()
        with pytest.raises(NotImplementedError):
            ext.extract(digital_pdf)


class TestOCRExtractor:
    """Tests for the OCR extractor (v0.2.0 placeholder)."""

    def test_not_implemented(self, digital_pdf: Path) -> None:
        """Should raise NotImplementedError."""
        ext = OCRExtractor()
        with pytest.raises(NotImplementedError):
            ext.extract(digital_pdf)


class TestLLMExtractor:
    """Tests for the LLM extractor (v0.2.0 placeholder)."""

    def test_not_implemented(self, digital_pdf: Path) -> None:
        """Should raise NotImplementedError."""
        ext = LLMExtractor()
        with pytest.raises(NotImplementedError):
            ext.extract(digital_pdf)
