#!/usr/bin/env python3
"""Extract heading classification features from benchmark PDFs.

For each text line in each PDF, extracts font-level features and labels
it as heading (1) or body (0) based on ground truth markdown.

Output: heading_features.jsonl — one JSON object per line per doc.
"""

import json
import os
import re
import sys
from pathlib import Path

import fitz

HOME = Path.home()
BENCH_ROOT = HOME / "Projects/opendataloader-bench"
PDF_DIR = BENCH_ROOT / "pdfs"
GT_DIR = BENCH_ROOT / "ground-truth/markdown"
OUTPUT = Path(__file__).parent.parent / "heading_features.jsonl"

# Add pdfmux to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from pdfmux.headings import _build_font_census, _normalize


def extract_gt_headings(gt_path: Path) -> set[str]:
    """Extract normalized heading texts from ground truth markdown."""
    gt = gt_path.read_text(encoding="utf-8")
    headings = re.findall(r"^#{1,6}\s+(.*)", gt, re.MULTILINE)
    return {_normalize(h) for h in headings if len(h.strip()) >= 2}


def extract_features(doc_id: str) -> list[dict]:
    """Extract per-line features from a PDF document."""
    pdf_path = PDF_DIR / f"{doc_id}.pdf"
    gt_path = GT_DIR / f"{doc_id}.md"

    if not pdf_path.exists() or not gt_path.exists():
        return []

    gt_headings = extract_gt_headings(gt_path)
    if not gt_headings:
        return []  # skip docs without GT headings (MHS not applicable)

    doc = fitz.open(str(pdf_path))
    features = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_height = page.rect.height
        page_width = page.rect.width

        if page_height <= 0 or page_width <= 0:
            continue

        body_size, candidates = _build_font_census(page)
        if body_size <= 0:
            continue

        for c in candidates:
            text = c.text.strip()
            if len(text) < 2:
                continue

            norm = _normalize(text)
            is_heading = 1 if norm in gt_headings else 0

            # Also check partial matches (GT heading starts with this text)
            if not is_heading:
                for gt_h in gt_headings:
                    if gt_h.startswith(norm) and len(norm) / max(len(gt_h), 1) > 0.7:
                        is_heading = 1
                        break

            feat = {
                "doc_id": doc_id,
                "page_num": page_num,
                "text": text[:60],
                "label": is_heading,
                # Font features
                "size_ratio": round(c.size / body_size, 4) if body_size > 0 else 1.0,
                "abs_size": round(c.size, 1),
                "body_size": round(body_size, 1),
                "is_bold": int(c.is_bold),
                # Text features
                "text_length": len(text),
                "word_count": len(text.split()),
                "has_period": int(text.rstrip().endswith(".")),
                "is_all_caps": int(text.isupper() and any(ch.isalpha() for ch in text)),
                "is_numeric": int(text.strip().strip(".").isdigit()),
                "starts_with_number": int(bool(re.match(r"^\d+[\.\)]\s", text))),
                # Position features
                "y_position_pct": round(c.y_position / page_height, 4) if page_height > 0 else 0.5,
                "x_position_pct": round(getattr(c, "x_position", 0) / page_width, 4) if page_width > 0 else 0.0,
                # Derived features
                "char_density": round(
                    sum(1 for ch in text if not ch.isspace()) / max(len(text), 1), 4
                ),
                "has_colon": int(":" in text),
                "has_question_mark": int("?" in text),
            }
            features.append(feat)

    doc.close()
    return features


def main():
    all_features = []
    doc_ids = sorted(f.stem for f in GT_DIR.glob("*.md"))

    for i, doc_id in enumerate(doc_ids):
        feats = extract_features(doc_id)
        all_features.extend(feats)
        if (i + 1) % 20 == 0:
            print(f"  processed {i + 1}/{len(doc_ids)} docs...", file=sys.stderr)

    # Write output
    with open(OUTPUT, "w") as f:
        for feat in all_features:
            f.write(json.dumps(feat) + "\n")

    # Summary
    total = len(all_features)
    positives = sum(1 for f in all_features if f["label"] == 1)
    print(f"Total lines: {total}")
    print(f"Headings: {positives} ({positives/total*100:.1f}%)")
    print(f"Body: {total - positives} ({(total-positives)/total*100:.1f}%)")
    print(f"Docs with features: {len(set(f['doc_id'] for f in all_features))}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
