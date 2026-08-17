# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Fixed
- **Vertical metrics mismatch** — OS/2 `sTypoAscender`/`sTypoDescender` now match `hhea` ascent/descent exactly, and `usWinAscent` was raised to prevent glyph clipping. `fsSelection` bit 7 (USE_TYPO_METRICS) is now set so modern renderers use consistent line-spacing across apps and operating systems.
- **Missing stylistic set descriptions** — ss01 through ss07 now have accurate description strings in the font's name table, based on directly inspecting each set's actual glyph substitutions (not assumed): ss01 alternate g, ss02 alternate Greek alpha, ss03 alternate R, ss04/ss05 alternate K/k variants, ss06 alternate rounded forms (C,D,G,O,Q,b), ss07 alternate e/g.

### Added
- `docs/design/README.md` — the full design specification, previously referenced by README and CONTRIBUTING but missing, causing broken links
- `scripts/qa.sh` — working fontbakery wrapper script, tested against the actual shipped fonts

### Fixed (previous)
- ROADMAP.md's v0.5 section previously restated specific numbers from an earlier, superseded design direction — now references `docs/design/` as the single source of truth instead of duplicating values that could drift out of sync

## [0.1.0] — Foundation release

### Added
- Initial public release: nine weights (Thin, Light, Regular, Medium, Bold, Black, Italic, Medium Italic, Bold Italic)
- Verified against the Gold Standard design specification (Helvetica structure / Frutiger apertures / Roboto screen-rendering discipline)
- Full repository documentation: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, ROADMAP, NOTICE

### Notes
- This release is built on Roboto's original outlines (Copyright Google Inc., Apache License 2.0), renamed and verified — not yet hand-redrawn. See [NOTICE.md](./NOTICE.md) for full attribution and [ROADMAP.md](./ROADMAP.md) for the plan toward original letterforms.
