# Changelog

All notable changes to Sky are documented here. Version numbers reflect actual design maturity — see [ROADMAP.md](./ROADMAP.md).

## [Unreleased]

### Website
- **Fixed: the site was rendering stale, pre-v0.3 fonts.** `website/index.html` embedded six base64 WOFF2 fonts that predated the −12% condensing (e.g. Regular H advance 1421u vs 1250u in v0.3) and still carried the old `sxHeight` of 1082. Italic styles were not embedded at all, so italics were browser-synthesised. The page now loads WOFF2 files generated from the shipped `fonts/*.ttf` (outlines and advance widths verified identical), with TTF fallback.
- All 9 styles wired via `@font-face` with correct weight/style mapping (100/300/400/500/700/900 upright; 400/500/700 italic), `font-display: swap`, and a preload for Regular. `index.html` drops from 1.1 MB to ~56 KB.
- Rebuilt the page, still a single static file with no build step and no third-party requests: type tester (editable text, weight, italic, size, line height, tracking, small caps / old-style figures / fractions, presets), weight waterfall for all nine styles, to-scale metrics diagram (cap 1456, x-height 990, ascender 1536, descender −427, 68% ratio, tabular digits), browsable glyph grid with inspector, honest originality status (v0.3 shipped; v0.5 in progress with H, E, F, I, L, T, Z, N, M, l), and download table with TTF + WOFF2 per style and the specimen PDF.
- Responsive layout (desktop to 390px mobile), system dark mode with a saved toggle, skip link, semantic landmarks, labelled controls, WCAG AA contrast (accent darkened from #5B7A99 to #4A6680 in light mode), `prefers-reduced-motion`. Meta description, canonical URL, Open Graph / Twitter card (`og.png`), and an SVG favicon drawn from Sky Bold's S.
- Added `scripts/make-webfonts.py` to regenerate `website/fonts/` (TTF copies, WOFF2, LICENSE/NOTICE) from `fonts/` so the site can't drift from the release files again.

### Changed — v0.5 letter #2: O / o
- **O and o rebuilt symmetric in all 9 styles.** The v0.2 x-height scaling had leaked into the capital O (bottom stroke 148u vs top 164u in Regular; lower bowl squarer than the upper; upper-left and upper-right handles mismatched), and the overshoot re-correction had moved only the top of o (top 154u vs bottom 139u). Each glyph is now its own-weight Roboto v2.138 outline put through only Sky's documented transforms (x ≈ 0.88 onto the v0.3 bounds; o: y × 0.915 onto −20 / 1007). Regular now measures O 164 / 163u, o 139 / 139u. Advance widths, side bearings, overshoot locks and kerning unchanged.
- **Spec change, approved by Gagan on 18 Nov 2026: squarer O/o (option B).** Off-curve points move toward each arc's tangent corner. Uprights use t = 0.12 (Regular squareness O 0.10 → 0.21, o 0.06 → 0.18). Each italic gets the t that matches its upright partner's squareness when de-slanted: Italic 0.148 / 0.141, Medium Italic 0.149 / 0.145, Bold Italic 0.148 / 0.147.
- 89 composite glyphs built on O/o (Ö, ó, ọ, ő, о, ο, …) inherit the new shapes.
- `scripts/glyphs/rebuild_O_o.py` (with `o_tension.json`) is reproducible; it needs Roboto v2.138 unhinted.

### Fixed — family repair of the v0.2 x-height scaling
- **Caps, figures and cap-height symbols restored to their foundation proportions in all 9 styles (516–533 glyphs per style, plus ~480 composites each through their components).** v0.2 had multiplied every point between the baseline and y ≈ 1104 by 0.898 in *every* glyph, so capitals kept their tops but lost a tenth of everything below. In Regular, the H bar sat at 605–746 (141u) instead of 673–830 (157u); E/F/A bars and B/P/R bowls were likewise low and thin; C, G, Q, D, U, S, 0, 3, 8 had bottom strokes ~10% lighter than the top. All of these now match Roboto v2.138 + Sky's transforms exactly (mean outline distance 13–20u → 0.2u).
- Detection is by measurement, glyph by glyph, against the same-weight Roboto. Lowercase, small caps / unicase, old-style figures, numerators / denominators, combining marks and below-cap punctuation keep the intended v0.2 x-height scaling.
- Corner-softening is re-applied and verified (every orthogonal corner is a 9u chamfer again; v0.3 had 8u below the zone line). The H and the other corner-softened letters keep their modification. Condensing, advance widths, spacing and kerning are byte-identical.
- Italic stems are no longer kinked at the zone line (9.6° below / 7.5° above → 8.6–8.7° throughout).
- Added `scripts/glyphs/repair_v02_zone.py` and `scripts/build-v05-repair.py`, which rebuild the v0.5 fonts from the v0.3 release in order.

### Fixed — metrics
- **Italic angle:** `post.italicAngle` −12° → **−8.66°**, the slant measured on the stems, with the hhea caret 100/21 → 2048/312 to match, in Italic, Medium Italic and Bold Italic. Roboto's true stem slant is 9.86°; the −12% condensing makes it 8.66°. fontbakery `caret_slope` goes from WARN to PASS.
- **Left side bearings:** hmtx lsb now equals the outline's xMin for every glyph. In v0.3, 1,302–1,436 glyphs per font disagreed by 2–18u (almost all accented composites). Rendering in Chrome / unhinted FreeType is unchanged; this fixes the metadata that hinting and hmtx-based tools use. Added `scripts/fix_metrics.py`.

### Notes
- Website font files (`website/fonts/`) regenerated from these fonts with `scripts/make-webfonts.py`.
- Found, not changed (decisions open): accented composites have advance widths that don't match their base letters (typically 6–36u wider in Regular) (spacing inconsistency from v0.3); c, e, s are still top-heavy (queued); Ø/Œ and C/G/Q/D don't yet carry the O/o tension; period, comma and other x-height-relative punctuation keep the v0.2 scaling.

---

## [0.3.0] — Horizontal condensing

### Changed
- **−12% horizontal width reduction across all 9 fonts** — x-coordinates scaled to 88% uniformly; y-coordinates untouched (x-height, cap height, ascenders, descenders all preserved). Advance widths and left side bearings scaled proportionally. Result: H advance moves from ~97% of cap height to ~85%, landing between Helvetica (~73%) and the original Roboto foundation (~97%). Letters are more compact and refined without feeling compressed.
- Applied to all weights: Thin, Light, Regular, Medium, Bold, Black, Italic, MediumItalic, BoldItalic.
- Website fonts updated to match.

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
