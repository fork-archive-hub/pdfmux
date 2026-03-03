"""Post-processing — clean extracted text and score confidence."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ProcessedResult:
    """Result of post-processing extracted text."""

    text: str
    confidence: float  # 0.0 - 1.0
    page_count: int
    warnings: list[str]


def clean_and_score(raw_text: str, page_count: int) -> ProcessedResult:
    """Clean extracted text and compute a confidence score.

    Cleaning steps:
    1. Normalize whitespace (collapse multiple blank lines)
    2. Fix common extraction artifacts
    3. Remove control characters
    4. Score confidence based on output quality signals

    Args:
        raw_text: Raw text from an extractor.
        page_count: Number of pages in the source PDF.

    Returns:
        ProcessedResult with cleaned text and confidence score.
    """
    warnings: list[str] = []

    text = raw_text

    # Remove control characters (except newlines and tabs)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Collapse 3+ consecutive blank lines into 2
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    # Fix broken words (hyphenation at line breaks)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Remove trailing whitespace from lines
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Strip leading/trailing whitespace from the whole document
    text = text.strip()

    # Compute confidence score
    confidence = _compute_confidence(text, page_count, warnings)

    return ProcessedResult(
        text=text,
        confidence=confidence,
        page_count=page_count,
        warnings=warnings,
    )


def _compute_confidence(text: str, page_count: int, warnings: list[str]) -> float:
    """Compute a confidence score for the extracted text.

    Checks:
    - Text completeness (chars per page)
    - Encoding quality (mojibake detection)
    - Structure preservation (headings, lists)
    - Whitespace sanity
    """
    if not text or page_count == 0:
        warnings.append("Empty output — extraction may have failed")
        return 0.0

    score = 1.0

    # Text completeness: expect at least ~200 chars per page for a typical document
    chars_per_page = len(text) / page_count
    if chars_per_page < 50:
        score -= 0.3
        warnings.append(f"Very little text extracted ({chars_per_page:.0f} chars/page)")
    elif chars_per_page < 200:
        score -= 0.1
        warnings.append(f"Low text density ({chars_per_page:.0f} chars/page)")

    # Encoding quality: check for common mojibake patterns
    mojibake_patterns = [r"â€", r"Ã©", r"Ã¨", r"â€™", r"ï¿½"]
    mojibake_count = sum(len(re.findall(p, text)) for p in mojibake_patterns)
    if mojibake_count > 10:
        score -= 0.3
        warnings.append(f"Possible encoding issues detected ({mojibake_count} patterns)")
    elif mojibake_count > 0:
        score -= 0.1

    # Structure: presence of Markdown headings is a good sign
    headings = len(re.findall(r"^#+\s", text, re.MULTILINE))
    if headings > 0:
        score += 0.05  # Bonus for preserved structure

    # Whitespace sanity: too many consecutive spaces suggests layout issues
    wide_spaces = len(re.findall(r"  {5,}", text))
    if wide_spaces > 20:
        score -= 0.1
        warnings.append("Excessive whitespace — layout extraction may be imperfect")

    return max(0.0, min(1.0, score))
