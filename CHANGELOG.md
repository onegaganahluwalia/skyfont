# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Changed
- **Corner softening applied to H, E, F, I, L, T, Z, N, M, l** — Roboto's stock construction uses perfectly sharp 90° corners on straight-stemmed letters. Applied a small, consistent geometric chamfer (9 units at 2048 UPM) at every sharp corner, per the design spec's "microscopic optical softening" principle. This is a real, verified geometric modification — not a redraw from nothing, but a deliberate, describable change to the actual outline data, distinct from stock Roboto. Visually confirmed intact across all 9 weights before shipping.
- Remaining letters with curved construction (O, n, and the rest of the alphabet) require a different, curve-aware technique — not yet applied. See ROADMAP.md.

## [Previous unreleased fixes]

### Fixed
- Vertical metrics mismatch (OS/2/hhea sync, usWinAscent, USE_TYPO_METRICS)
- Missing stylistic set descriptions (ss01-ss07), based on direct inspection of actual glyph substitutions

### Added
- `docs/design/README.md`, `scripts/qa.sh`

## [0.1.0] — Foundation release

### Added
- Initial public release: nine weights, verified against the Gold Standard design specification
- Full repository documentation

### Notes
- Built on Roboto's original outlines (Copyright Google Inc., Apache License 2.0). See NOTICE.md.
