"""Tests for LangChain and LlamaIndex integrations."""

from __future__ import annotations

from pathlib import Path

import pytest


class TestLangChainLoader:
    """Tests for PDFMuxLoader."""

    def test_loader_init(self) -> None:
        """PDFMuxLoader should initialize without langchain installed."""
        from pdfmux.integrations.langchain import PDFMuxLoader

        loader = PDFMuxLoader("test.pdf", quality="fast")
        assert loader.path == Path("test.pdf")
        assert loader.quality == "fast"

    def test_loader_requires_langchain(self, digital_pdf: Path) -> None:
        """load() should raise ImportError if langchain-core is missing."""
        from pdfmux.integrations.langchain import PDFMuxLoader

        loader = PDFMuxLoader(digital_pdf)
        # langchain-core is not installed in test env
        with pytest.raises(ImportError, match="langchain-core"):
            loader.load()

    def test_loader_default_quality(self) -> None:
        """Default quality should be 'standard'."""
        from pdfmux.integrations.langchain import PDFMuxLoader

        loader = PDFMuxLoader("test.pdf")
        assert loader.quality == "standard"


class TestLlamaIndexReader:
    """Tests for PDFMuxReader."""

    def test_reader_init(self) -> None:
        """PDFMuxReader should initialize without llama-index installed."""
        from pdfmux.integrations.llamaindex import PDFMuxReader

        reader = PDFMuxReader(quality="fast")
        assert reader.quality == "fast"

    def test_reader_requires_llamaindex(self, digital_pdf: Path) -> None:
        """load_data() should raise ImportError if llama-index-core is missing."""
        from pdfmux.integrations.llamaindex import PDFMuxReader

        reader = PDFMuxReader()
        with pytest.raises(ImportError, match="llama-index-core"):
            reader.load_data(digital_pdf)

    def test_reader_default_quality(self) -> None:
        """Default quality should be 'standard'."""
        from pdfmux.integrations.llamaindex import PDFMuxReader

        reader = PDFMuxReader()
        assert reader.quality == "standard"
