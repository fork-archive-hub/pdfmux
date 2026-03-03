# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-03

### Added
- PDF type detection (digital vs scanned, table detection)
- PyMuPDF fast extractor for digital PDFs (~0.01s/page)
- Markdown output formatter optimized for LLM consumption
- CLI with `readable convert` command (single file and batch)
- MCP server via `readable serve` for AI agent integration
- Confidence scoring with `--confidence` flag
- Post-processing: whitespace normalization, broken-word fixing, encoding cleanup
- Quality presets: fast, standard, high
- GitHub Actions CI (lint → test → build)
- Docker multi-stage build
