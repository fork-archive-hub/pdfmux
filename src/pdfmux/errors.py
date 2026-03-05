"""Error hierarchy — flat, explicit, catch-friendly.

All pdfmux exceptions inherit from PdfmuxError so callers can:

    try:
        pdfmux.extract_text("report.pdf")
    except pdfmux.PdfmuxError as e:
        print(f"pdfmux failed: {e}  (code={e.code})")

Each exception has a `.code` class attribute for programmatic handling.

Propagation rules:
    - FileError        → raise immediately, nothing to retry
    - ExtractorNotAvailable → log + try next extractor in registry
    - ExtractionError  → log + try next extractor in registry
    - FormatError      → raise immediately, caller picked bad format
    - AuditError       → log + skip audit, return unaudited result
    - OCRTimeoutError  → log + skip page, mark as unrecovered
"""

from __future__ import annotations


class PdfmuxError(Exception):
    """Base exception for all pdfmux errors."""

    code: str = "PDFMUX_ERROR"


class FileError(PdfmuxError):
    """PDF file not found, not a PDF, corrupted, or unreadable.

    Specific codes:
        PDF_NOT_FOUND  — file does not exist
        PDF_CORRUPTED  — file exists but can't be opened as PDF
        PDF_ENCRYPTED  — file is password-protected
        PDF_INVALID    — file is not a PDF at all
    """

    code: str = "PDF_NOT_FOUND"

    def __init__(self, message: str, *, code: str = "PDF_NOT_FOUND") -> None:
        super().__init__(message)
        self.code = code


class ExtractionError(PdfmuxError):
    """An extractor failed to produce output.

    Codes:
        EXTRACTION_ERROR    — general extraction failure
        PARTIAL_EXTRACTION  — some pages failed but others succeeded
    """

    code: str = "EXTRACTION_ERROR"

    def __init__(self, message: str, *, code: str = "EXTRACTION_ERROR") -> None:
        super().__init__(message)
        self.code = code


class ExtractorNotAvailable(PdfmuxError):  # noqa: N818
    """An optional extractor dependency is not installed.

    Includes install instructions in the message:
        ExtractorNotAvailable("RapidOCR not installed. pip install pdfmux[ocr]")
    """

    code: str = "NO_EXTRACTOR"


class FormatError(PdfmuxError):
    """Invalid or unsupported output format requested."""

    code: str = "FORMAT_ERROR"


class AuditError(PdfmuxError):
    """Per-page quality audit failed (non-fatal in pipeline)."""

    code: str = "AUDIT_ERROR"


class OCRTimeoutError(PdfmuxError):
    """OCR processing exceeded time limit."""

    code: str = "OCR_TIMEOUT"
