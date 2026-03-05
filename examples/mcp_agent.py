#!/usr/bin/env python3
"""MCP server usage — how to configure pdfmux as a tool for AI agents.

This example shows the MCP server configuration for Claude Desktop,
Cursor, and other MCP-compatible AI tools.

To start the server manually (for testing):
    pdfmux serve

For production, configure your AI tool to spawn the server automatically.
"""

from __future__ import annotations

import json


def print_claude_config() -> None:
    """Print the Claude Desktop configuration for pdfmux."""
    config = {
        "mcpServers": {
            "pdfmux": {
                "command": "pdfmux",
                "args": ["serve"],
            }
        }
    }

    print("=== Claude Desktop / Cursor Config ===")
    print("Add this to your MCP settings:\n")
    print(json.dumps(config, indent=2))
    print()


def print_available_tools() -> None:
    """Print the available MCP tools."""
    print("=== Available MCP Tools ===\n")

    tools = [
        {
            "name": "convert_pdf",
            "description": "Convert a PDF to Markdown text",
            "example": {
                "file_path": "/path/to/document.pdf",
                "quality": "standard",
            },
        },
        {
            "name": "analyze_pdf",
            "description": "Quick triage — classify and audit without extraction",
            "example": {
                "file_path": "/path/to/document.pdf",
            },
        },
        {
            "name": "batch_convert",
            "description": "Convert all PDFs in a directory",
            "example": {
                "directory": "/path/to/pdf/folder/",
                "quality": "standard",
            },
        },
    ]

    for tool in tools:
        print(f"  {tool['name']}")
        print(f"    {tool['description']}")
        print(f"    Example args: {json.dumps(tool['example'])}")
        print()


def print_usage_examples() -> None:
    """Print example agent interactions."""
    print("=== Example Agent Interactions ===\n")

    examples = [
        ("Triage a PDF", "analyze_pdf", '{"file_path": "/tmp/report.pdf"}'),
        ("Extract text", "convert_pdf", '{"file_path": "/tmp/report.pdf"}'),
        ("Fast extraction", "convert_pdf", '{"file_path": "/tmp/report.pdf", "quality": "fast"}'),
        ("Batch convert", "batch_convert", '{"directory": "/tmp/invoices/"}'),
    ]

    for desc, tool, args in examples:
        print(f"  {desc}:")
        print(f"    Tool: {tool}")
        print(f"    Args: {args}")
        print()


if __name__ == "__main__":
    print_claude_config()
    print_available_tools()
    print_usage_examples()
