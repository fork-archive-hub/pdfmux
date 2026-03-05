#!/usr/bin/env python3
"""Batch PDF processing — convert a directory of PDFs with progress tracking.

Usage:
    python examples/batch_processing.py path/to/pdf/directory/

Requires:
    pip install pdfmux
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from pdfmux.pipeline import process_batch


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python examples/batch_processing.py <directory>")
        sys.exit(1)

    pdf_dir = Path(sys.argv[1])
    if not pdf_dir.is_dir():
        print(f"Error: {pdf_dir} is not a directory")
        sys.exit(1)

    pdfs = list(pdf_dir.glob("*.pdf")) + list(pdf_dir.glob("*.PDF"))
    if not pdfs:
        print(f"No PDF files found in {pdf_dir}")
        sys.exit(0)

    print(f"Processing {len(pdfs)} PDFs from {pdf_dir}...\n")

    start = time.perf_counter()
    success = 0
    failed = 0

    for path, result_or_error in process_batch(pdfs, output_format="markdown"):
        if isinstance(result_or_error, Exception):
            print(f"  FAIL  {path.name}: {result_or_error}")
            failed += 1
        else:
            r = result_or_error
            ocr_info = f", {len(r.ocr_pages)} OCR'd" if r.ocr_pages else ""
            print(
                f"  OK    {path.name} — "
                f"{r.page_count} pages, "
                f"{r.confidence:.0%} confidence{ocr_info}"
            )

            # Save output
            out_path = path.with_suffix(".md")
            out_path.write_text(r.text, encoding="utf-8")
            success += 1

    elapsed = time.perf_counter() - start
    print(f"\nDone in {elapsed:.1f}s: {success} converted, {failed} failed")


if __name__ == "__main__":
    main()
