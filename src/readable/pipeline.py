"""Pipeline — tiered routing logic that picks the best extractor per PDF.

This is the core of Readable. Instead of using one extraction method,
we detect the PDF type and route to the optimal extractor:

  Digital, clean → PyMuPDF (free, 0.01s/page)
  Has tables → Docling (free, 0.3-3s/page) [v0.2.0]
  Scanned → OCR pipeline (free, 1-5s/page) [v0.2.0]
  Complex/fallback → Gemini Flash ($0.01-0.05) [v0.2.0]
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from readable.detect import PDFClassification, classify
from readable.extractors.fast import FastExtractor
from readable.formatters.markdown import format_markdown
from readable.postprocess import ProcessedResult, clean_and_score


@dataclass
class ConversionResult:
    """Full result of converting a PDF."""

    text: str
    format: str
    confidence: float
    extractor_used: str
    page_count: int
    warnings: list[str]
    classification: PDFClassification


def process(
    file_path: str | Path,
    output_format: str = "markdown",
    quality: str = "standard",
    show_confidence: bool = False,
) -> ConversionResult:
    """Process a PDF through the tiered extraction pipeline.

    Args:
        file_path: Path to the PDF file.
        output_format: Output format — "markdown" (default), "json", "csv".
        quality: Quality preset — "fast" (rule-based only), "standard" (auto),
                 "high" (force ML-based).
        show_confidence: Whether to include confidence info in output.

    Returns:
        ConversionResult with extracted text and metadata.
    """
    file_path = Path(file_path)

    # Step 1: Classify the PDF
    classification = classify(file_path)

    # Step 2: Route to the best extractor
    extractor, raw_text = _route_and_extract(file_path, classification, quality)

    # Step 3: Post-process and score confidence
    processed = clean_and_score(raw_text, classification.page_count)

    # Step 4: Format output
    formatted = _format_output(processed, output_format, file_path, show_confidence)

    return ConversionResult(
        text=formatted,
        format=output_format,
        confidence=processed.confidence,
        extractor_used=extractor,
        page_count=classification.page_count,
        warnings=processed.warnings,
        classification=classification,
    )


def _route_and_extract(
    file_path: Path,
    classification: PDFClassification,
    quality: str,
) -> tuple[str, str]:
    """Route to the appropriate extractor based on PDF classification.

    Returns:
        Tuple of (extractor_name, raw_text).
    """
    # Fast mode: always use PyMuPDF
    if quality == "fast":
        ext = FastExtractor()
        return ext.name, ext.extract(file_path)

    # Standard/high mode: route based on classification
    if classification.is_digital and not classification.has_tables:
        # Simple digital PDF — use fast extractor
        ext = FastExtractor()
        return ext.name, ext.extract(file_path)

    if classification.has_tables:
        # Has tables — try fast extractor first (MVP), Docling in v0.2.0
        # TODO(v0.2.0): Use TableExtractor for table-heavy PDFs
        ext = FastExtractor()
        return ext.name, ext.extract(file_path)

    if classification.is_scanned:
        # Scanned PDF — OCR needed
        # TODO(v0.2.0): Use OCRExtractor
        # For now, try fast extractor (will get whatever text is available)
        ext = FastExtractor()
        raw = ext.extract(file_path)
        if len(raw.strip()) < 100:
            raise RuntimeError(
                "PDF appears to be scanned/image-based but OCR is not yet available. "
                "OCR support is coming in v0.2.0. Install with: pip install readable[ocr]"
            )
        return ext.name, raw

    if classification.is_mixed:
        # Mixed: extract digital pages with PyMuPDF
        # TODO(v0.2.0): OCR the scanned pages, merge results
        ext = FastExtractor()
        return ext.name, ext.extract(file_path, pages=classification.digital_pages)

    # Default fallback
    ext = FastExtractor()
    return ext.name, ext.extract(file_path)


def _format_output(
    processed: ProcessedResult,
    output_format: str,
    source_path: Path,
    show_confidence: bool,
) -> str:
    """Format the processed text into the requested output format."""
    if output_format == "markdown":
        text = format_markdown(processed.text, source=str(source_path))
        if show_confidence:
            confidence_note = (
                f"\n\n---\n"
                f"*Conversion confidence: {processed.confidence:.0%} "
                f"({processed.page_count} pages)*"
            )
            if processed.warnings:
                confidence_note += "\n" + "\n".join(f"- ⚠ {w}" for w in processed.warnings)
            text += confidence_note
        return text

    if output_format == "json":
        raise NotImplementedError("JSON output format is planned for v0.2.0")

    if output_format == "csv":
        raise NotImplementedError("CSV output format is planned for v0.2.0")

    raise ValueError(f"Unknown output format: {output_format}")
