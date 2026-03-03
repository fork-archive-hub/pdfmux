"""Tests for the extraction pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest

from readable.pipeline import process


def test_process_digital_pdf(digital_pdf: Path) -> None:
    """Processing a digital PDF should return Markdown text."""
    result = process(digital_pdf)
    assert result.text
    assert result.format == "markdown"
    assert result.page_count == 2
    assert result.confidence > 0
    assert result.extractor_used == "pymupdf4llm (fast)"


def test_process_with_confidence(digital_pdf: Path) -> None:
    """--confidence flag should add confidence info to output."""
    result = process(digital_pdf, show_confidence=True)
    assert "confidence" in result.text.lower() or "Conversion confidence" in result.text


def test_process_fast_quality(digital_pdf: Path) -> None:
    """Fast quality should always use PyMuPDF."""
    result = process(digital_pdf, quality="fast")
    assert result.extractor_used == "pymupdf4llm (fast)"


def test_process_unsupported_format(digital_pdf: Path) -> None:
    """Unsupported output formats should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown output format"):
        process(digital_pdf, output_format="xml")


def test_process_json_not_implemented(digital_pdf: Path) -> None:
    """JSON format should raise NotImplementedError (v0.2.0)."""
    with pytest.raises(NotImplementedError):
        process(digital_pdf, output_format="json")


def test_process_multi_page(multi_page_pdf: Path) -> None:
    """Multi-page PDFs should process correctly."""
    result = process(multi_page_pdf)
    assert result.page_count == 5
    assert len(result.text) > 100
