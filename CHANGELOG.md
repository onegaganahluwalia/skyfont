# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Fixed
- **OS/2 `sxHeight` metadata corrected** — all 9 fonts now report `sxHeight = 990` (68.0% of cap height), matching the actual outline x-height. Previously the field still held the pre-reduction Roboto value of 1082 (74.3%), causing applications that read this metric for line-spacing calculations to use the wrong value.

### Verified
- Weight interpolation confirmed: stem widths progress cleanly across the family (Thin 36u → Light 105u → Regular 175u → Medium 234u → Bold 283u → Black 333u). Step sizes compress slightly in the upper range (+69/+70/+59/+49/+50u), which is the expected roll-off for heavy weights. No non-monotonic steps.
- All vertical metrics (OS/2 typoAscender/Descender ↔ hhea ascent/descent, USE_TYPO_METRICS bit) confirmed consistent across all 9 weights.

---

### Added (from previous sessions)
- `docs/design/README.md` — the full design specification, previously referenced by README and CONTRIBUTING but missing, causing broken links
- Verified-value annotations in the spec, documenting exactly which targets have been measured against the shipped font versus not yet re-checked

### Fixed (from previous sessions)
- ROADMAP.md's v0.5 section previously restated specific numbers from an earlier, superseded design direction — now references `docs/design/` as the single source of truth instead of duplicating values that could drift out of sync

## [0.1.0] — Foundation release

### Added
- Initial public release: nine weights (Thin, Light, Regular, Medium, Bold, Black, Italic, Medium Italic, Bold Italic)
- Verified against the Gold Standard design specification (Helvetica structure / Frutiger apertures / Roboto screen-rendering discipline)
- Full repository documentation: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, ROADMAP, NOTICE

### Notes
- This release is built on Roboto's original outlines (Copyright Google Inc., Apache License 2.0), renamed and verified — not yet hand-redrawn. See [NOTICE.md](./NOTICE.md) for full attribution and [ROADMAP.md](./ROADMAP.md) for the plan toward original letterforms.
