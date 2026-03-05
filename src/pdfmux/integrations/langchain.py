"""LangChain document loader for pdfmux.

Usage:
    from pdfmux.integrations.langchain import PDFMuxLoader

    loader = PDFMuxLoader("report.pdf")
    docs = loader.load()
    # → list[Document] with metadata

Requires:
    pip install pdfmux[langchain]
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class PDFMuxLoader:
    """LangChain document loader that wraps pdfmux.load_llm_context().

    Converts each pdfmux chunk into a LangChain Document with metadata
    including source, title, page range, token estimate, and confidence.

    Args:
        path: Path to the PDF file.
        quality: Extraction quality preset ("fast", "standard", "high").

    Example::

        from pdfmux.integrations.langchain import PDFMuxLoader

        loader = PDFMuxLoader("report.pdf", quality="standard")
        docs = loader.load()
        for doc in docs:
            print(f"{doc.metadata['title']}: {len(doc.page_content)} chars")
    """

    def __init__(self, path: str | Path, *, quality: str = "standard") -> None:
        self.path = Path(path)
        self.quality = quality

    def load(self) -> list:
        """Load the PDF and return a list of LangChain Documents.

        Returns:
            List of langchain_core.documents.Document objects.

        Raises:
            ImportError: If langchain-core is not installed.
        """
        try:
            from langchain_core.documents import Document
        except ImportError:
            raise ImportError(
                "langchain-core is required for PDFMuxLoader. "
                "Install it with: pip install pdfmux[langchain]"
            ) from None

        import pdfmux

        chunks = pdfmux.load_llm_context(self.path, quality=self.quality)

        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk["text"],
                metadata={
                    "source": str(self.path),
                    "title": chunk["title"],
                    "page_start": chunk["page_start"],
                    "page_end": chunk["page_end"],
                    "tokens": chunk["tokens"],
                    "confidence": chunk["confidence"],
                },
            )
            documents.append(doc)

        return documents

    def lazy_load(self):
        """Lazy-load documents one at a time (generator).

        Yields:
            langchain_core.documents.Document objects.
        """
        yield from self.load()
