# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Added
- `docs/design/README.md` — the full design specification, previously referenced by README and CONTRIBUTING but missing, causing broken links
- Verified-value annotations in the spec, documenting exactly which targets have been measured against the shipped font versus not yet re-checked

### Fixed
- ROADMAP.md's v0.5 section previously restated specific numbers from an earlier, superseded design direction — now references `docs/design/` as the single source of truth instead of duplicating values that could drift out of sync

## [0.1.0] — Foundation release

### Added
- Initial public release: nine weights (Thin, Light, Regular, Medium, Bold, Black, Italic, Medium Italic, Bold Italic)
- Verified against the Gold Standard design specification (Helvetica structure / Frutiger apertures / Roboto screen-rendering discipline)
- Full repository documentation: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, ROADMAP, NOTICE

### Notes
- This release is built on Roboto's original outlines (Copyright Google Inc., Apache License 2.0), renamed and verified — not yet hand-redrawn. See [NOTICE.md](./NOTICE.md) for full attribution and [ROADMAP.md](./ROADMAP.md) for the plan toward original letterforms.
