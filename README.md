# pdfmux

The smart PDF-to-Markdown router. One command, zero config.

```
PDF ──→ pdfmux ──→ Markdown
         │
         ├─ digital?  → PyMuPDF     (0.01s/pg, free)
         ├─ tables?   → Docling     (0.3s/pg, free)
         ├─ scanned?  → Surya OCR   (1-5s/pg, free)
         └─ complex?  → Gemini Flash (2-5s/pg, ~$0.01)
```

We don't convert PDFs. We route them to whichever tool converts them best.

90% of PDFs are digital — converted in milliseconds, for free.

## Install

```
pip install pdfmux
```

## Usage

```bash
# convert a pdf
pdfmux invoice.pdf
# ✓ invoice.pdf → invoice.md (2 pages, 0.02s)

# batch convert a directory
pdfmux ./docs/ -o ./output/

# json output with metadata
pdfmux report.pdf -f json

# start mcp server for ai agents
pdfmux serve
```

## How it works

pdfmux inspects each PDF, classifies it (digital, scanned, has tables, mixed),
and routes to the fastest extractor that can handle it well:

| PDF Type | Extractor | Speed | Cost |
|----------|-----------|-------|------|
| Digital | PyMuPDF | 0.01s/page | Free |
| Tables | Docling | 0.3-3s/page | Free |
| Scanned | Surya OCR | 1-5s/page | Free |
| Complex | Gemini Flash | 2-5s/page | ~$0.01/doc |

If an extractor isn't installed, pdfmux falls back to the next best option automatically.
No errors, no config. It just works.

## MCP Server

Give your AI agent the ability to read any PDF. Add to Claude Desktop or Cursor:

```json
{
  "mcpServers": {
    "pdfmux": {
      "command": "pdfmux",
      "args": ["serve"]
    }
  }
}
```

Exposes a single `convert_pdf` tool over stdio MCP. Your agent calls it, gets Markdown back.

## Optional extractors

The base install handles digital PDFs (the vast majority). Add extras for harder cases:

```bash
pip install pdfmux[tables]  # Docling — 97.9% table accuracy
pip install pdfmux[ocr]     # Surya OCR — scanned documents
pip install pdfmux[llm]     # Gemini Flash — complex layouts
pip install pdfmux[all]     # everything
```

## Why not just use X?

| Tool | Good at | Limitation |
|------|---------|-----------|
| Marker | GPU ML extraction | Overkill for simple digital PDFs |
| Docling | Tables | Slow on non-table documents |
| pymupdf4llm | Fast digital text | Can't handle scanned or complex layouts |
| **pdfmux** | Picking the right tool automatically | — |

pdfmux uses these tools. It doesn't compete with them — it orchestrates them.

## License

[MIT](LICENSE)
