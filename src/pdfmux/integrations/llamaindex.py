"""LlamaIndex document reader for pdfmux.

Usage:
    from pdfmux.integrations.llamaindex import PDFMuxReader

    reader = PDFMuxReader(quality="standard")
    docs = reader.load_data("report.pdf")
    # → list[Document] with metadata

Requires:
    pip install pdfmux[llamaindex]
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class PDFMuxReader:
    """LlamaIndex reader that wraps pdfmux.load_llm_context().

    Converts each pdfmux chunk into a LlamaIndex Document with metadata
    including source, title, page range, token estimate, and confidence.

    Args:
        quality: Extraction quality preset ("fast", "standard", "high").

    Example::

        from pdfmux.integrations.llamaindex import PDFMuxReader

        reader = PDFMuxReader(quality="standard")
        docs = reader.load_data("report.pdf")
        for doc in docs:
            print(f"{doc.metadata['title']}: {len(doc.text)} chars")
    """

    def __init__(self, *, quality: str = "standard") -> None:
        self.quality = quality

    def load_data(self, path: str | Path) -> list:
        """Load a PDF and return a list of LlamaIndex Documents.

        Args:
            path: Path to the PDF file.

        Returns:
            List of llama_index.core.schema.Document objects.

        Raises:
            ImportError: If llama-index-core is not installed.
        """
        try:
            from llama_index.core.schema import Document
        except ImportError:
            raise ImportError(
                "llama-index-core is required for PDFMuxReader. "
                "Install it with: pip install pdfmux[llamaindex]"
            ) from None

        import pdfmux

        path = Path(path)
        chunks = pdfmux.load_llm_context(path, quality=self.quality)

        documents = []
        for chunk in chunks:
            doc = Document(
                text=chunk["text"],
                metadata={
                    "source": str(path),
                    "title": chunk["title"],
                    "page_start": chunk["page_start"],
                    "page_end": chunk["page_end"],
                    "tokens": chunk["tokens"],
                    "confidence": chunk["confidence"],
                },
            )
            documents.append(doc)

        return documents
