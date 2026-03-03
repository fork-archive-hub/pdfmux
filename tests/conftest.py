"""Shared test fixtures."""

from __future__ import annotations

from pathlib import Path

import fitz
import pytest


@pytest.fixture
def digital_pdf(tmp_path: Path) -> Path:
    """Create a simple digital PDF for testing."""
    pdf_path = tmp_path / "digital_simple.pdf"
    doc = fitz.open()

    # Page 1: Simple text
    page = doc.new_page()
    text = (
        "# Introduction\n\n"
        "This is a sample PDF document created for testing purposes. "
        "It contains multiple paragraphs of text that should be "
        "extractable by the fast PyMuPDF extractor.\n\n"
        "## Section 1\n\n"
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."
    )
    page.insert_text((72, 72), text, fontsize=11)

    # Page 2: More text
    page2 = doc.new_page()
    text2 = (
        "## Section 2\n\n"
        "This is the second page of our test document. "
        "It demonstrates that the extractor can handle multi-page PDFs "
        "and maintain structure across pages.\n\n"
        "- Item one\n"
        "- Item two\n"
        "- Item three"
    )
    page2.insert_text((72, 72), text2, fontsize=11)

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def empty_pdf(tmp_path: Path) -> Path:
    """Create an empty PDF for edge case testing."""
    pdf_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def multi_page_pdf(tmp_path: Path) -> Path:
    """Create a 5-page digital PDF."""
    pdf_path = tmp_path / "multi_page.pdf"
    doc = fitz.open()

    for i in range(5):
        page = doc.new_page()
        text = (
            f"Page {i + 1} of 5\n\n"
            f"This is content on page {i + 1}. It contains enough text "
            f"to be classified as a digital page by our detection logic. "
            f"The quick brown fox jumps over the lazy dog. "
            f"Pack my box with five dozen liquor jugs."
        )
        page.insert_text((72, 72), text, fontsize=11)

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path
