# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Changed
- **Corner-softening extended to A, K, V, W, X, Y, k, v, w, x, z, and digits 1/4/7** — same verified technique as the first batch (H, E, F, I, L, T, Z, N, M, l), applied after confirming each is pure straight-line construction (safe for this exact method). 24 letters + 3 digits now carry this real, describable modification.
- Confirmed unsafe for this technique and left untouched: y, U, J (all mix curves with straight lines — corner-softening would risk distorting the curve).

### Previous unreleased work
- ~3.2% narrower spacing (deliberate design choice, not a fix)
- Vertical metrics fix, stylistic set descriptions
- `docs/design/README.md`, `scripts/qa.sh`, live website

## [0.1.0] — Foundation release

Initial public release: nine weights, verified against the Gold Standard design specification. Built on Roboto's original outlines (Apache License 2.0). See NOTICE.md.
