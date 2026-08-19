# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Changed
- **Sky is now ~3.2% narrower than its Roboto foundation** — a deliberate design choice (not a bug fix) toward a quieter, more restrained reading rhythm. Implemented as proportional side-bearing tightening (12%, scaled per-glyph) across the entire family, applied to advance width and glyph position only — no letterform outlines were compressed or distorted. Verified against tight letter combinations for collision risk before shipping.
- Fixed a real bug hit during this work: one obscure combining glyph could get a negative advance width under aggressive tightening, which crashed font compilation. Now guarded against — any glyph whose resulting width would fall below a safe minimum is left untouched instead.

### Previous unreleased work
- Corner-softening on H, E, F, I, L, T, Z, N, M, l
- Vertical metrics fix (OS/2/hhea sync, USE_TYPO_METRICS)
- Stylistic set descriptions (ss01-ss07)
- `docs/design/README.md`, `scripts/qa.sh`, website with live font tester

## [0.1.0] — Foundation release

Initial public release: nine weights, verified against the Gold Standard design specification. Built on Roboto's original outlines (Apache License 2.0). See NOTICE.md.
