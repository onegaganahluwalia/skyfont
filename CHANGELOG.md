# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Changed
- **Default line-height increased from 1.32x to 1.45x** — a deliberate, evidence-backed choice for sustained reading comfort, not an arbitrary preference. This is baked directly into the font's ascent/descent metrics rather than using the lineGap field, specifically because lineGap is handled inconsistently across platforms (desktop apps, browsers, and Windows all treat it differently) — baking it into ascent/descent instead means every application respects it identically. Caught this cross-platform inconsistency risk via fontbakery before shipping the simpler (wrong) version.

### Previous unreleased work
- Fixed asymmetric overshoot on lowercase o/c/e/s (real typographic bug, not a preference)
- Corner-softening on 24 letters + 3 digits
- ~3.2% narrower spacing (deliberate design choice)
- Vertical metrics sync, stylistic set descriptions, docs/design spec, QA tooling, live website

## [0.1.0] — Foundation release

Initial public release: nine weights, verified against the Gold Standard design specification. Built on Roboto's original outlines (Apache License 2.0). See NOTICE.md.
