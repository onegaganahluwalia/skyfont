# Roadmap

This roadmap is the honest record of how original Sky's design is at any given point — see the README for why that matters. Every milestone below states plainly what's Roboto-derived versus hand-drawn.

## v0.1 — Foundation (current)

- Verified, renamed Roboto foundation (Apache 2.0)
- Metrics and construction checked against the Gold Standard spec (Helvetica structure / Frutiger apertures / Roboto screen discipline)
- Nine weights shipping: Thin, Light, Regular, Medium, Bold, Black, Italic, Medium Italic, Bold Italic
- **Status: 0% hand-drawn.** Every glyph is Roboto's original outline, renamed.

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
