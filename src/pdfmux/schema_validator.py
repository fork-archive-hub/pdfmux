"""Schema-validated extraction — Instructor pattern for PDFs.

Extract structured data from PDFs and validate against a JSON schema.
When validation fails, retry extraction with targeted prompts.

Usage:
    pdfmux convert invoice.pdf --schema invoice.json
    pdfmux convert invoice.pdf --schema invoice  # built-in preset

Built-in presets: invoice, receipt, contract, resume, paper
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Maximum retry attempts for schema validation
MAX_RETRIES = 3

# Built-in schema presets
PRESETS: dict[str, dict] = {
    "invoice": {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string"},
            "date": {"type": "string"},
            "due_date": {"type": "string"},
            "vendor": {"type": "string"},
            "customer": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "total": {"type": "number"},
                    },
                },
            },
            "subtotal": {"type": "number"},
            "tax": {"type": "number"},
            "total": {"type": "number"},
            "currency": {"type": "string"},
        },
        "required": ["invoice_number", "total"],
    },
    "receipt": {
        "type": "object",
        "properties": {
            "merchant": {"type": "string"},
            "date": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                    },
                },
            },
            "total": {"type": "number"},
            "payment_method": {"type": "string"},
        },
        "required": ["merchant", "total"],
    },
    "contract": {
        "type": "object",
        "properties": {
            "parties": {"type": "array", "items": {"type": "string"}},
            "effective_date": {"type": "string"},
            "expiration_date": {"type": "string"},
            "terms": {"type": "array", "items": {"type": "string"}},
            "governing_law": {"type": "string"},
            "signatures": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["parties"],
    },
    "resume": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "summary": {"type": "string"},
            "experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string"},
                        "title": {"type": "string"},
                        "dates": {"type": "string"},
                        "description": {"type": "string"},
                    },
                },
            },
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "institution": {"type": "string"},
                        "degree": {"type": "string"},
                        "dates": {"type": "string"},
                    },
                },
            },
            "skills": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["name"],
    },
    "paper": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
            "abstract": {"type": "string"},
            "keywords": {"type": "array", "items": {"type": "string"}},
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "heading": {"type": "string"},
                        "content": {"type": "string"},
                    },
                },
            },
            "references": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["title"],
    },
}


def load_schema(schema_ref: str) -> dict:
    """Load a JSON schema from a preset name or file path.

    Args:
        schema_ref: Either a preset name (invoice, receipt, etc.)
                   or a path to a JSON schema file.

    Returns:
        JSON schema dict.

    Raises:
        ValueError: If schema can't be loaded.
    """
    # Check presets first
    if schema_ref in PRESETS:
        return PRESETS[schema_ref]

    # Try as file path
    path = Path(schema_ref)
    if path.is_file():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Failed to load schema from {path}: {e}")

    valid_presets = ", ".join(PRESETS.keys())
    raise ValueError(
        f"Schema '{schema_ref}' not found. "
        f"Valid presets: {valid_presets}. Or provide a path to a JSON schema file."
    )


def validate_against_schema(data: dict, schema: dict) -> list[str]:
    """Validate extracted data against a JSON schema.

    Simple validation without jsonschema dependency.
    Checks required fields and basic type matching.

    Returns:
        List of validation error strings (empty = valid).
    """
    errors = []

    if not isinstance(data, dict):
        return ["Expected object, got " + type(data).__name__]

    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: {field}")
        elif isinstance(data[field], str) and not data[field].strip():
            errors.append(f"Required field is empty: {field}")

    # Check property types
    properties = schema.get("properties", {})
    for field, field_schema in properties.items():
        if field not in data or data[field] is None:
            continue

        expected_type = field_schema.get("type")
        value = data[field]

        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"Field '{field}' should be string, got {type(value).__name__}")
        elif expected_type == "number" and not isinstance(value, (int, float)):
            errors.append(f"Field '{field}' should be number, got {type(value).__name__}")
        elif expected_type == "array" and not isinstance(value, list):
            errors.append(f"Field '{field}' should be array, got {type(value).__name__}")
        elif expected_type == "object" and not isinstance(value, dict):
            errors.append(f"Field '{field}' should be object, got {type(value).__name__}")

    return errors


def get_preset_names() -> list[str]:
    """Return all available preset schema names."""
    return list(PRESETS.keys())
