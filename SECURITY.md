# Security Policy

## Reporting a vulnerability

Font files are parsed by operating systems, browsers, and design applications — a malformed font can, in rare cases, be a real attack surface (malformed glyph tables, invalid OpenType feature code, etc.). Website/build tooling vulnerabilities are the more common concern for a project like this.

If you find a security issue in:
- **The font binaries themselves** (malformed tables, parser-crashing input, etc.)
- **The website** (sky-type.org or wherever it's hosted)
- **Build tooling or CI/CD**

Please report it privately rather than opening a public issue. Use GitHub's private vulnerability reporting (Security tab → Report a vulnerability) so it can be addressed before public disclosure.

## Supported versions

Only the latest released minor version receives security fixes during the pre-1.0 phase. This will expand to a proper support matrix once Sky reaches 1.0.

## Response time

Maintainers aim to acknowledge reports within 5 business days. This is a community project without dedicated security staff — response times reflect that honestly.
