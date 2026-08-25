# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Fixed
- **Tabular digit alignment, broken by an earlier change** — stock Roboto's digits are tabular by design (all exactly equal width, for tables/prices/data alignment). The spacing-tightening work applied a generic per-glyph proportional adjustment that treated digits like any other letter, which broke their intentional uniform width (each digit's natural left-bearing differs, so a uniform *percentage* shift produced different *absolute* shifts per digit). Found via direct measurement with real text shaping (not assumed), confirmed against a clean copy of stock Roboto to verify it wasn't a pre-existing issue. Fixed by re-centering each digit's ink within a shared target width (1114 units, preserving the original ~3.2% narrowing intent) instead of the generic per-glyph method. Verified with a realistic aligned-numbers render before shipping.
- Also verified during this work: kerning (inherited from Roboto) is real and functioning correctly on all classic problem pairs (LT, PA, AT, etc.), and remains collision-free even combined with the spacing and digit changes.

### Previous unreleased work
- Default line-height increased to 1.45x (baked into ascent/descent, not lineGap, for cross-platform consistency)
- Fixed asymmetric overshoot on lowercase o/c/e/s
- Corner-softening on 24 letters + 3 digits
- ~3.2% narrower spacing (deliberate design choice)
- Reading mode + recent work section added to website

## [0.1.0] — Foundation release

Initial public release: nine weights, verified against the Gold Standard design specification. Built on Roboto's original outlines (Apache License 2.0). See NOTICE.md.
