# pdfmux

The smart PDF-to-Markdown router. One command, zero config, best extractor per document.

> We don't convert PDFs. We route them to whichever tool converts them best.

## Install

```bash
pip install pdfmux
```

## Usage

```bash
# Convert a PDF to Markdown
pdfmux invoice.pdf

# Batch convert a directory
pdfmux ./docs/ -o ./output/

# JSON output with metadata
pdfmux report.pdf -f json

# Show confidence score
pdfmux report.pdf --confidence

# Start MCP server for AI agents
pdfmux serve
```

## How It Works

pdfmux auto-detects your PDF type and routes to the optimal extractor:

| PDF Type | Extractor | Speed | Cost |
|----------|-----------|-------|------|
| Digital (clean text) | PyMuPDF | 0.01s/page | Free |
| Tables | Docling | 0.3-3s/page | Free |
| Scanned | Surya OCR | 1-5s/page | Free |
| Complex | Gemini Flash | 2-5s/page | ~$0.01/doc |

90% of PDFs are digital — converted in milliseconds, for free.

## MCP Server

Add to your Claude / Cursor config:

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

Your AI agent can now read PDFs natively.

## Optional Extractors

```bash
pip install pdfmux[tables]  # Docling — 97.9% table accuracy
pip install pdfmux[ocr]     # Surya — scanned PDF support
pip install pdfmux[llm]     # Gemini Flash — hardest cases
pip install pdfmux[all]     # Everything
```

## Why Not Just Use X?

| Tool | When to Use It Instead |
|------|----------------------|
| **Marker** | You need GPU-accelerated ML extraction for everything |
| **Docling** | You only process table-heavy documents |
| **pymupdf4llm** | You only have digital PDFs and want zero dependencies |
| **pdfmux** | You want one tool that picks the right method automatically |

## License

MIT
