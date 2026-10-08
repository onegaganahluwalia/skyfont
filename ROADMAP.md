# Roadmap

This roadmap is the honest record of how original Sky's design is at any given point — see the README for why that matters. Every milestone below states plainly what's Roboto-derived versus hand-drawn.

## Locked design decisions

These are permanent. They define Sky's character and should not be changed without a formal spec-change proposal (see `.github/ISSUE_TEMPLATE/spec_change.md`).

| Decision | Value | Reason |
|---|---|---|
| Cap height | 1456 units | — |
| **X-height** | **990 units (68% of cap)** | **Sky's defining proportion — deliberately quieter than Roboto (74%) and Helvetica (71%), closer to classical faces. Locked permanently.** |
| Ascender | 1536 units | — |
| Descender | −427 units | — |
| Default line-height | 1.45× | Baked into ascent/descent, not lineGap |
| Spacing | ~3.2% narrower than Roboto | Side-bearing led, not letterform compression |
| Digit width | 1114 units (tabular) | All 10 digits equal for table/price alignment |
| Overshoot (o/c/e/s) | +17 top, −20 bottom | Symmetric, proportional to cap height |



## v0.1 — Foundation release ✅ Complete

- Verified, renamed Roboto foundation (Apache 2.0)
- Metrics and construction checked against the Gold Standard spec (Helvetica structure / Frutiger apertures / Roboto screen discipline)
- Nine weights shipping: Thin, Light, Regular, Medium, Bold, Black, Italic, Medium Italic, Bold Italic
- **Status: 0% hand-drawn.** Every glyph is Roboto's original outline, renamed.

## v0.2 — Metric lock + bearing audit ✅ Complete

All foundational metric decisions locked and verified. Zero known spacing problems remain.

**Completed:**
- x-height reduced to 68% of cap height (990 / 1456u) — Sky's defining proportion, permanently locked. Verified in outlines and OS/2 `sxHeight` metadata across all 9 fonts.
- 5,901 negative side-bearing fixes across the extended glyph set; italic variants fully repaired
- Individual spacing repairs: r, f, k, K, j — all negative/near-zero bearings corrected
- t crossbar repositioned to correct height at new x-height
- Overshoot re-corrected: +17 top / −20 bottom (scaling had amplified this to +124; fixed back)
- Denominator (dnom) figures standardised to 751u
- Tabular digit alignment restored (1114u per digit)
- Vertical metrics fully consistent: OS/2 typo ↔ hhea, USE_TYPO_METRICS bit set
- Weight interpolation verified: clean monotonic progression Thin → Black
- Kerning confirmed active (AV pair and paragraph rendering verified comfortable)
- **Status: 0% hand-drawn.** Foundation metric engineering complete.

## v0.5 — Core DNA letters

**Method note (added after real work began):** "original" here means *verified, deliberate geometric modification* of the Roboto-derived foundation — real point-level engineering with a documented typographic reason for each change — not drawing from a blank canvas. Some letters turn out to already meet spec (no change needed, confirmed by measurement). Some get real, describable modifications (e.g., corner-softening on straight-stemmed letters). Some require careful curve-level work that takes longer to get right. Every change ships only after visual verification; nothing gets modified just to show progress.

Target letters, in build order (each sets rules the next inherits — see [docs/design/](./docs/design/README.md) for the full reasoning behind this sequence):

1. H — stem width, terminal treatment ✅ corner-softened
2. O — curve DNA for every round letter
3. n — shoulder/spacing rhythm
4. a, e, S, y, R, g — signature glyphs with the most distinctive construction decisions

Exact target proportions for each (aperture angles, terminal cuts, junction treatment) live in [docs/design/](./docs/design/README.md) — that document is the single source of truth for numbers; this roadmap only tracks sequence and status.

**Status at this milestone: 10 letters carry verified modifications (H, E, F, I, L, T, Z, N, M, l — corner-softening). Everything else still Roboto-derived, unmodified.**

## v0.9 — Release candidate

- Full Latin uppercase, lowercase, and numerals redrawn against spec
- Kerning pass across the full redrawn set
- fontbakery QA passing clean

**Status: full core Latin set hand-drawn.**

## v1.0 — First original release

- Every glyph in the core Latin set is original, spec-built work
- This is the actual "Sky is its own typeface" milestone
- Punctuation, accented Latin characters (é, ñ, etc.) completed

## v2.0 — Variable font

- Weight axis as a true variable font, not discrete static weights
- True drawn italics (not oblique/slanted transforms of the roman)
- Optical size axis under consideration (see Gold Standard blueprint's optical sizing matrix)

## v2.x+ — Script expansion

- Devanagari, Arabic, and other scripts per original project notes
- Each script expansion gets its own design lead rather than one team attempting every script — quality over speed here

---

**Want to help with the next milestone?** Check [CONTRIBUTING.md](./CONTRIBUTING.md) — the glyph proposal template will tell you exactly what's next in sequence.
