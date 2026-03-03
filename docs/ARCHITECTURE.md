# Architecture — Readable

See the full architecture document at:
`Business Agents/products/readable/01-spec/ARCHITECTURE.md`

## Quick Reference

```
readable CLI / MCP server
    → pipeline.py (tiered routing)
        → detect.py (classify PDF type)
        → extractors/fast.py (PyMuPDF — 90% of PDFs)
        → extractors/tables.py (Docling — v0.2.0)
        → extractors/ocr.py (Surya — v0.2.0)
        → extractors/llm.py (Gemini Flash — v0.2.0)
    → postprocess.py (clean + confidence score)
    → formatters/markdown.py (output)
```
