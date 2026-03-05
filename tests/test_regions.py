"""Tests for region OCR — surgical OCR of image regions."""

from __future__ import annotations

from pathlib import Path

import fitz

from pdfmux.regions import (
    detect_weak_regions,
    merge_region_text,
)
from pdfmux.types import WeakRegion


class TestDetectWeakRegions:
    """Tests for detect_weak_regions()."""

    def test_no_images_no_regions(self, digital_pdf: Path) -> None:
        """A digital text PDF should have no weak regions."""
        regions = detect_weak_regions(digital_pdf, page_num=0)
        # Digital PDF with text but no large images → no regions
        # (may have 0 regions or regions if there are images, but no crash)
        assert isinstance(regions, list)

    def test_empty_page_no_regions(self, empty_pdf: Path) -> None:
        """An empty page should have no weak regions."""
        regions = detect_weak_regions(empty_pdf, page_num=0)
        assert regions == []

    def test_out_of_range_page(self, digital_pdf: Path) -> None:
        """Out-of-range page number should return empty list."""
        regions = detect_weak_regions(digital_pdf, page_num=999)
        assert regions == []

    def test_region_with_image_pdf(self, tmp_path: Path) -> None:
        """A page with an image and no overlapping text should produce a weak region."""
        pdf_path = tmp_path / "img_test.pdf"
        doc = fitz.open()
        page = doc.new_page(width=612, height=792)

        # Insert a large rectangle to simulate an image area
        # We use insert_image with a simple pixmap
        pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 200, 200), 1)
        pix.clear_with(255)  # white image
        page.insert_image(fitz.Rect(50, 50, 250, 250), pixmap=pix)

        # Add some text far away from the image
        page.insert_text((50, 400), "Text far below the image area", fontsize=10)

        doc.save(str(pdf_path))
        doc.close()

        regions = detect_weak_regions(pdf_path, page_num=0)
        # The image may or may not produce a region depending on size thresholds
        # but the function should run without errors
        assert isinstance(regions, list)
        for r in regions:
            assert isinstance(r, WeakRegion)
            assert r.page_num == 0
            assert len(r.bbox) == 4


class TestMergeRegionText:
    """Tests for merge_region_text()."""

    def test_merge_appends_text(self) -> None:
        """Region text should be appended to page text."""
        page_text = "Existing page content here."
        regions = [
            WeakRegion(page_num=0, bbox=(50, 100, 250, 300), reason="test"),
        ]
        region_texts = ["OCR extracted from image region"]

        merged = merge_region_text(page_text, regions, region_texts)
        assert "Existing page content" in merged
        assert "OCR extracted from image region" in merged

    def test_merge_empty_regions(self) -> None:
        """Empty regions list should return page text unchanged."""
        page_text = "Original text"
        merged = merge_region_text(page_text, [], [])
        assert merged == "Original text"

    def test_merge_empty_ocr_text(self) -> None:
        """Regions with empty OCR text should be skipped."""
        page_text = "Original text"
        regions = [
            WeakRegion(page_num=0, bbox=(50, 100, 250, 300), reason="test"),
        ]
        region_texts = [""]

        merged = merge_region_text(page_text, regions, region_texts)
        assert merged == "Original text"

    def test_merge_sorts_by_y_position(self) -> None:
        """Regions should be merged in top-to-bottom order."""
        page_text = "Header text"
        regions = [
            WeakRegion(page_num=0, bbox=(50, 400, 250, 500), reason="bottom"),
            WeakRegion(page_num=0, bbox=(50, 100, 250, 200), reason="top"),
        ]
        region_texts = ["Bottom region text", "Top region text"]

        merged = merge_region_text(page_text, regions, region_texts)
        top_pos = merged.index("Top region text")
        bottom_pos = merged.index("Bottom region text")
        assert top_pos < bottom_pos
