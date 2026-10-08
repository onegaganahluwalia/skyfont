# Changelog

All notable changes to Sky are documented here.

## [Unreleased]

### Fixed — comprehensive bearing audit
- **319 glyphs with negative side-bearings in Regular (5,901 fixes across all 9 weights)** — the spacing-tightening applied earlier treated every glyph generically, including extended Latin characters (accented letters, Vietnamese diacritics, specialty symbols like florin, longs, horn variants). These glyphs had different natural bearings and the proportional reduction broke many into negative territory. Fixed by batch-correcting all remaining negative lsb/rsb values. Italic variants were most severely affected (1,100–1,200 broken glyphs each) because italic glyphs naturally overhang more, making them more sensitive to bearing reduction. Zero remaining negative bearing problems confirmed after fix.
- Website fonts refreshed to current build.

### Previous — Update 11
- j lsb fixed (was −66, colliding with preceding letters)
- t crossbar raised to correct position at x-height after 68% reduction

## [0.1.0] — Foundation release
Built on Roboto's original outlines (Apache License 2.0). See NOTICE.md.
