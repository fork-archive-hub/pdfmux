# Changelog

## 0.2.2 (2026-03-04)

### Added
- **Graphical PDF detection** — detects image-heavy PDFs (pitch decks, infographics) and routes to OCR/LLM instead of fast extraction
- **Honest confidence scoring** — confidence now reflects actual extraction quality, not just text presence. Graphical PDFs with missing image content score lower.
- **Actionable warnings** — clear messages when extraction is limited, with specific `pip install pdfmux[ocr]` or `pdfmux[llm]` suggestions
- **MCP server quality metadata** — AI agents now receive confidence score and warnings alongside extracted text
- **Spaced-text cleanup** — fixes common PDF artifact where text renders as "W i t h  o v e r" → "With over"

### Fixed
- Detection no longer classifies image-heavy "digital" PDFs as fully extractable
- Confidence no longer reports 100% on graphical PDFs where image content was missed
- FastExtractor now falls back to raw fitz when pymupdf4llm returns empty (fixes certain PDF encodings)
- bench command now shows honest confidence that matches pipeline routing

## 0.2.1 (2026-03-04)

### Added
- **`pdfmux doctor`** — check installed extractors, versions, and API keys
- **`pdfmux bench`** — benchmark all available extractors on a PDF side by side

### Fixed
- Suppressed upstream pymupdf4llm "Consider using pymupdf_layout" noise from all commands

## 0.2.0 (2026-03-03)

First public release.

### Added
- **Smart routing** — auto-detect PDF type and pick the best extractor
- **PyMuPDF extractor** — digital PDFs at 0.01s/page
- **Docling extractor** — 97.9% table accuracy (optional: `pdfmux[tables]`)
- **Surya OCR extractor** — scanned PDF support (optional: `pdfmux[ocr]`)
- **Gemini Flash extractor** — complex layout fallback (optional: `pdfmux[llm]`)
- **Mixed PDF handling** — digital pages + scanned pages merged automatically
- **Output formats** — Markdown, JSON, CSV
- **Quality presets** — fast, standard, high
- **Batch conversion** — convert entire directories
- **MCP server** — built-in stdio server for AI agents
- **Confidence scoring** — text completeness, encoding quality, structure checks
- **Graceful fallback** — missing extractors fall back silently to next best
