"""Markdown formatter — the primary output format.

Markdown is the optimal format for LLM consumption:
- 60.7% LLM accuracy vs 44.3% for CSV
- 20-35% better RAG accuracy vs HTML/plain text
- 10-15% token savings vs JSON
- Safe to chunk at heading boundaries
"""

from __future__ import annotations

import re


def format_markdown(text: str, add_frontmatter: bool = False, source: str = "") -> str:
    """Format extracted text as clean Markdown.

    Args:
        text: Post-processed extracted text.
        add_frontmatter: Whether to add YAML frontmatter with metadata.
        source: Source file path (for frontmatter).

    Returns:
        Clean Markdown string.
    """
    result = text

    # Ensure consistent heading style (ATX-style with space after #)
    result = re.sub(r"^(#{1,6})([^ #\n])", r"\1 \2", result, flags=re.MULTILINE)

    # Ensure blank line before headings
    result = re.sub(r"([^\n])\n(#{1,6} )", r"\1\n\n\2", result)

    # Normalize list markers to `-`
    result = re.sub(r"^[ \t]*[*•]\s", "- ", result, flags=re.MULTILINE)

    if add_frontmatter and source:
        frontmatter = f"---\nsource: {source}\nconverter: readable\n---\n\n"
        result = frontmatter + result

    return result
