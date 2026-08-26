# Changelog

All notable changes to Sky are documented here.

## [Unreleased]

### Changed — the most significant structural decision in the project
- **X-height locked at 68% of cap height — Sky's defining proportion.** Stock Roboto sits at ~74%, Helvetica at ~71%, classical faces at 60–66%. Sky's 68% is a deliberate choice toward quieter, more considered proportions — taller caps relative to lowercase, less digital density. Every weight's scale factor computed from its own actual measurements. Only x-height zone coordinates were scaled; caps, ascenders, and descenders untouched. Verified per-boundary before shipping.

### Fixed (follow-up to x-height change, same session)
- **Overshoot on o/c/e/s re-corrected after x-height scaling.** The earlier tapered overshoot correction was applied before the x-height change — scaling the whole x-height zone then amplified the overshoot from the intended +17 units to +124, making round letters protrude far too far above x-height. Corrected back to +17 (proportionally matching the bottom overshoot of 20) using the same tapered approach to avoid curve distortion.

### Fixed (same push)
- **Denominator figure (dnom) width inconsistency** — same class of bug as the tabular digit fix. Denominators now uniform at 751 units, matching numerator figures for correct fraction alignment.

### Previous unreleased work
- Tabular digit alignment restored
- Default line-height 1.45x
- Fixed asymmetric overshoot on o/c/e/s (before x-height change; re-corrected above)
- Corner-softening on 24 letters + 3 digits
- ~3.2% narrower spacing

## [0.1.0] — Foundation release
Built on Roboto's original outlines (Apache License 2.0). See NOTICE.md.
