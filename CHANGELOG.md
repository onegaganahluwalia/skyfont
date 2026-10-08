# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

Nothing pending.

---

## [0.2.0] — x-height milestone

This release marks the completion of Sky's foundational metric work. The 68% x-height is now fully locked in outlines, metadata, and documentation. Zero known bearing problems across the extended glyph set.

### Changed
- **x-height reduced from ~74% → 68% of cap height** — Sky's defining proportion, deliberately lower than Roboto (74%) and Helvetica (71%). Applied via per-weight outline scaling (y-coordinates in the 0–990u zone only; caps, ascenders, descenders untouched). Per-weight scale factors computed individually.
- **OS/2 `sxHeight` corrected to 990** — all 9 fonts now report `sxHeight = 990` (68.0% of cap height), matching the actual outline x-height. Previously held the pre-reduction Roboto value of 1082 (74.3%), causing line-spacing miscalculation in applications that read this metric.

### Fixed
- **5,901 negative side-bearing fixes** across the extended glyph set. 319 problems in Regular alone; italic variants had 1,100–1,200 broken glyphs from the spacing script hitting italic overhang geometry. Zero known bearing problems remain.
- **r rsb** — was 13u (near-zero) and negative in Italic variants → fixed to 110u across all weights
- **f, k rsb** — was negative in multiple weights → fixed to 80u
- **K capital rsb** — BoldItalic was −159u → fixed to 90u across all weights
- **j lsb** — was −66u (visible collision risk) → fixed to 60u
- **t crossbar** — repositioned to correct height after x-height scaling
- **Overshoot re-corrected** after x-height scaling had amplified the +12u target to +124u → restored to +17u top / −20u bottom
- **Denominator (dnom) figures** — standardised to uniform 751u across all weights
- **Tabular digit alignment** — spacing tightening had broken equal-width alignment; re-centred to 1114u per digit

### Verified
- Weight interpolation confirmed clean: Thin 36u → Light 105u → Regular 175u → Medium 234u → Bold 283u → Black 333u. Step sizes compress naturally in the upper range (+69/+70/+59/+49/+50u); no non-monotonic steps.
- Kerning active and working — AV pair confirmed, full paragraph rendering comfortable.
- All vertical metrics consistent: OS/2 typoAscender/Descender ↔ hhea ascent/descent synced, USE_TYPO_METRICS bit set across all 9 fonts.
- Aperture openness: c at 43.9°, e at ~42° (both exceed target).

### Documentation
- `docs/design/README.md` — x-height and stem-ratio entries updated to reflect verified v0.2 values
- ROADMAP.md updated — v0.2 milestone section reflects actual work completed

---

## [0.1.0] — Foundation release

### Added
- Initial public release: nine weights (Thin, Light, Regular, Medium, Bold, Black, Italic, Medium Italic, Bold Italic)
- Corner-softening on 24 letters + 3 digits (H, E, F, I, L, T, Z, N, M, l, A, K, V, W, X, Y, k, v, w, x, z + digits 1, 4, 7)
- Spacing tightened ~3.2% via proportional side-bearing reduction (letterforms not compressed)
- Overshoot fixed symmetrically on o/c/e/s using tapered technique to avoid curve kinks
- Default line-height set to 1.45× baked into ascent/descent metrics (not lineGap)
- Vertical metrics: OS/2 typo ↔ hhea sync, USE_TYPO_METRICS bit set
- Stylistic set descriptions ss01–ss07 added from actual GSUB inspection
- Full repository documentation: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, ROADMAP, NOTICE
- GitHub Actions auto-deploy to GitHub Pages

### Notes
- Built on Roboto's original outlines (Copyright Google Inc., Apache License 2.0), renamed and verified — not yet hand-redrawn. See [NOTICE.md](./NOTICE.md) for full attribution and [ROADMAP.md](./ROADMAP.md) for the plan toward original letterforms.
