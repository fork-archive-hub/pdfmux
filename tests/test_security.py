"""Tests for security limits — file size, page count, timeouts."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from pdfmux.errors import FileError
from pdfmux.pipeline import process


class TestSecurityLimits:
    """Tests for pipeline security checks."""

    def test_file_size_limit(self, tmp_path: Path) -> None:
        """Files exceeding MAX_FILE_SIZE_MB should be rejected."""
        import fitz

        # Create a small valid PDF
        pdf_path = tmp_path / "large.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), "Test content")
        doc.save(str(pdf_path))
        doc.close()

        # Patch the limit to be very small (0MB = reject everything)
        with patch("pdfmux.pipeline.MAX_FILE_SIZE_MB", 0):
            with pytest.raises(FileError, match="File too large"):
                process(pdf_path)

    def test_page_count_limit(self, digital_pdf: Path) -> None:
        """PDFs exceeding MAX_PAGE_COUNT should be rejected."""
        # Patch the limit to be very small
        with patch("pdfmux.pipeline.MAX_PAGE_COUNT", 1):
            with pytest.raises(FileError, match="Too many pages"):
                process(digital_pdf)  # digital_pdf has 2 pages

    def test_normal_pdf_passes_limits(self, digital_pdf: Path) -> None:
        """Normal PDFs should pass all security checks."""
        # Default limits (500MB, 10000 pages) should not block a normal PDF
        result = process(digital_pdf)
        assert result.text
        assert result.confidence > 0
