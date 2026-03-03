"""PDF type detection — classify a PDF to route it to the best extractor."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import fitz  # PyMuPDF


@dataclass
class PDFClassification:
    """Result of classifying a PDF document."""

    is_digital: bool = False
    is_scanned: bool = False
    is_mixed: bool = False
    has_tables: bool = False
    page_count: int = 0
    languages: list[str] = field(default_factory=list)
    confidence: float = 0.0
    digital_pages: list[int] = field(default_factory=list)
    scanned_pages: list[int] = field(default_factory=list)


def classify(file_path: str | Path) -> PDFClassification:
    """Classify a PDF to determine the best extraction strategy.

    Strategy:
    1. Open with PyMuPDF, read metadata
    2. Per page: check if text is extractable (digital) or image-only (scanned)
    3. Check for table patterns (ruled lines, aligned blocks)
    4. Return classification with confidence
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")
    if not file_path.suffix.lower() == ".pdf":
        raise ValueError(f"Not a PDF file: {file_path}")

    doc = fitz.open(str(file_path))
    result = PDFClassification(page_count=len(doc))

    digital_pages = []
    scanned_pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        images = page.get_images(full=True)

        # A page is "digital" if it has meaningful extractable text
        # Heuristic: > 50 chars of text means digital
        if len(text) > 50:
            digital_pages.append(page_num)
        elif images:
            scanned_pages.append(page_num)
        else:
            # Empty page or minimal content — treat as digital
            digital_pages.append(page_num)

    result.digital_pages = digital_pages
    result.scanned_pages = scanned_pages

    total = len(doc)
    if total == 0:
        result.confidence = 0.0
        doc.close()
        return result

    digital_ratio = len(digital_pages) / total

    if digital_ratio >= 0.8:
        result.is_digital = True
        result.confidence = min(0.95, digital_ratio)
    elif digital_ratio <= 0.2:
        result.is_scanned = True
        result.confidence = min(0.95, 1 - digital_ratio)
    else:
        result.is_mixed = True
        result.confidence = 0.7  # Mixed docs are harder to classify

    # Table detection: look for ruled lines or grid patterns
    result.has_tables = _detect_tables(doc)

    doc.close()
    return result


def _detect_tables(doc: fitz.Document) -> bool:
    """Heuristic table detection using line analysis.

    Checks for horizontal/vertical line patterns that suggest tables.
    """
    for page_num in range(min(len(doc), 5)):  # Check first 5 pages
        page = doc[page_num]
        drawings = page.get_drawings()

        horizontal_lines = 0
        vertical_lines = 0

        for drawing in drawings:
            for item in drawing.get("items", []):
                if item[0] == "l":  # Line
                    p1, p2 = item[1], item[2]
                    # Horizontal line: y-coordinates are similar
                    if abs(p1.y - p2.y) < 2 and abs(p1.x - p2.x) > 50:
                        horizontal_lines += 1
                    # Vertical line: x-coordinates are similar
                    elif abs(p1.x - p2.x) < 2 and abs(p1.y - p2.y) > 20:
                        vertical_lines += 1

        # If we see a grid pattern, it's likely a table
        if horizontal_lines >= 3 and vertical_lines >= 2:
            return True

    # Fallback: check for tab-separated or aligned text patterns
    for page_num in range(min(len(doc), 5)):
        page = doc[page_num]
        text = page.get_text("text")
        lines = text.split("\n")
        tab_lines = sum(1 for line in lines if "\t" in line or line.count("  ") >= 3)
        if tab_lines >= 3:
            return True

    return False
