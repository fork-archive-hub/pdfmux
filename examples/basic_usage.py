#!/usr/bin/env python3
"""Basic pdfmux usage — extract text, JSON, and LLM chunks from a PDF.

Usage:
    python examples/basic_usage.py path/to/file.pdf

Requires:
    pip install pdfmux
"""

from __future__ import annotations

import sys
from pathlib import Path

import pdfmux


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python examples/basic_usage.py <path-to-pdf>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    print(f"pdfmux {pdfmux.__version__}\n")

    # --- 1. Extract as Markdown ---
    print("=== Markdown extraction ===")
    text = pdfmux.extract_text(pdf_path)
    print(f"Extracted {len(text):,} characters")
    print(f"Preview: {text[:200]}...\n")

    # --- 2. Extract as structured JSON ---
    print("=== JSON extraction ===")
    data = pdfmux.extract_json(pdf_path)
    print(f"Pages: {data['page_count']}")
    print(f"Confidence: {data['confidence']:.0%}")
    print(f"Extractor: {data['extractor']}")
    print(f"Schema: {data['schema_version']}")
    if data["warnings"]:
        print(f"Warnings: {data['warnings']}")
    print()

    # --- 3. Extract as LLM-ready chunks ---
    print("=== LLM chunks ===")
    chunks = pdfmux.load_llm_context(pdf_path)
    print(f"Got {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}] {chunk['title']} — {chunk['tokens']} tokens (pages {chunk['page_start']}-{chunk['page_end']})")
    print()

    # --- 4. Quality presets ---
    print("=== Quality presets ===")
    for quality in ["fast", "standard"]:
        text = pdfmux.extract_text(pdf_path, quality=quality)
        print(f"  {quality}: {len(text):,} chars")


if __name__ == "__main__":
    main()
