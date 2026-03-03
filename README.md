# Readable

The smart PDF-to-Markdown router. One command, zero config, best extractor per document.

> We don't convert PDFs. We route them to whichever tool converts them best.

## Install

```bash
pip install readable
```

## Usage

```bash
# Convert a PDF to Markdown
readable invoice.pdf

# Batch convert a directory
readable ./docs/ -o ./output/

# Show confidence score
readable report.pdf --confidence

# Start MCP server for AI agents
readable serve
```

## How It Works

Readable auto-detects your PDF type and routes to the optimal extractor:

| PDF Type | Extractor | Speed | Cost |
|----------|-----------|-------|------|
| Digital (clean text) | PyMuPDF | 0.01s/page | Free |
| Tables | Docling (v0.2) | 0.3-3s/page | Free |
| Scanned | OCR (v0.2) | 1-5s/page | Free |
| Complex | Gemini Flash (v0.2) | 2-5s/page | ~$0.01/doc |

90% of PDFs are digital — converted in milliseconds, for free.

## MCP Server

Add to your Claude / Cursor config:

```json
{
  "mcpServers": {
    "readable": {
      "command": "readable",
      "args": ["serve"]
    }
  }
}
```

Your AI agent can now read PDFs natively.

## Why Not Just Use X?

| Tool | When to Use It Instead |
|------|----------------------|
| **Marker** | You need GPU-accelerated ML extraction for everything |
| **Docling** | You only process table-heavy documents |
| **pymupdf4llm** | You only have digital PDFs and want zero dependencies |
| **Readable** | You want one tool that picks the right method automatically |

## License

MIT
