"""Tests for schema-validated extraction."""

from __future__ import annotations

import json

import pytest

from pdfmux.schema_validator import (
    PRESETS,
    get_preset_names,
    load_schema,
    validate_against_schema,
)


class TestLoadSchema:
    def test_load_preset_invoice(self):
        schema = load_schema("invoice")
        assert schema["type"] == "object"
        assert "invoice_number" in schema["properties"]
        assert "total" in schema["required"]

    def test_load_preset_receipt(self):
        schema = load_schema("receipt")
        assert "merchant" in schema["properties"]

    def test_load_preset_resume(self):
        schema = load_schema("resume")
        assert "name" in schema["required"]

    def test_load_preset_paper(self):
        schema = load_schema("paper")
        assert "title" in schema["required"]
        assert "authors" in schema["properties"]

    def test_load_from_file(self, tmp_path):
        schema_data = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        path = tmp_path / "custom.json"
        path.write_text(json.dumps(schema_data))

        loaded = load_schema(str(path))
        assert loaded["required"] == ["name"]

    def test_load_invalid_preset(self):
        with pytest.raises(ValueError, match="not found"):
            load_schema("nonexistent_schema")

    def test_load_invalid_file(self):
        with pytest.raises(ValueError, match="not found"):
            load_schema("/nonexistent/path.json")

    def test_load_malformed_json(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("{invalid json")
        with pytest.raises(ValueError, match="Failed to load"):
            load_schema(str(path))


class TestValidateAgainstSchema:
    def test_valid_invoice(self):
        schema = PRESETS["invoice"]
        data = {
            "invoice_number": "INV-001",
            "total": 1500.00,
            "vendor": "Acme Corp",
        }
        errors = validate_against_schema(data, schema)
        assert errors == []

    def test_missing_required_field(self):
        schema = PRESETS["invoice"]
        data = {"vendor": "Acme Corp"}  # missing invoice_number and total
        errors = validate_against_schema(data, schema)
        assert any("invoice_number" in e for e in errors)
        assert any("total" in e for e in errors)

    def test_empty_required_field(self):
        schema = PRESETS["invoice"]
        data = {"invoice_number": "", "total": 100}
        errors = validate_against_schema(data, schema)
        assert any("empty" in e for e in errors)

    def test_wrong_type(self):
        schema = PRESETS["invoice"]
        data = {
            "invoice_number": "INV-001",
            "total": "not a number",
        }
        errors = validate_against_schema(data, schema)
        assert any("number" in e for e in errors)

    def test_non_dict_data(self):
        schema = PRESETS["invoice"]
        errors = validate_against_schema("not a dict", schema)
        assert len(errors) == 1

    def test_extra_fields_ok(self):
        schema = PRESETS["receipt"]
        data = {
            "merchant": "Coffee Shop",
            "total": 5.50,
            "extra_field": "should be fine",
        }
        errors = validate_against_schema(data, schema)
        assert errors == []

    def test_array_type_check(self):
        schema = PRESETS["resume"]
        data = {
            "name": "John Doe",
            "skills": "not an array",
        }
        errors = validate_against_schema(data, schema)
        assert any("array" in e for e in errors)

    def test_valid_resume(self):
        schema = PRESETS["resume"]
        data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "skills": ["Python", "ML"],
            "experience": [
                {
                    "company": "Acme",
                    "title": "Engineer",
                    "dates": "2020-2024",
                }
            ],
        }
        errors = validate_against_schema(data, schema)
        assert errors == []


class TestPresets:
    def test_all_presets_are_valid_schemas(self):
        for name, schema in PRESETS.items():
            assert "type" in schema, f"Preset '{name}' missing 'type'"
            assert "properties" in schema, f"Preset '{name}' missing 'properties'"

    def test_all_presets_have_required(self):
        for name, schema in PRESETS.items():
            assert "required" in schema, f"Preset '{name}' missing 'required'"
            assert len(schema["required"]) > 0

    def test_get_preset_names(self):
        names = get_preset_names()
        assert "invoice" in names
        assert "receipt" in names
        assert "contract" in names
        assert "resume" in names
        assert "paper" in names
        assert len(names) == 5
