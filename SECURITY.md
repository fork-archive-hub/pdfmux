# Security Policy

## Reporting a Vulnerability

**Do not open public issues for security vulnerabilities.**

Please report security vulnerabilities via GitHub's [private vulnerability reporting](https://github.com/NameetP/pdfmux/security/advisories/new).

You will receive a response within 48 hours. If the issue is confirmed, a patch will be released as soon as possible, typically within 7 days.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |
| < Latest | No       |

Only the latest release receives security updates. We recommend always using the latest version.

## Scope

The following are in scope for security reports:

- Arbitrary file read/write via crafted PDF input
- Path traversal in file handling
- Denial of service via malformed PDFs
- Dependency vulnerabilities in core dependencies
- Information leakage through error messages or logs

## Disclosure Policy

- We follow coordinated disclosure — please allow us time to patch before publishing
- Credit will be given in the release notes unless you prefer to remain anonymous
