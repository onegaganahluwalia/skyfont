# Notice

Sky is derived from **Roboto**, Copyright Google Inc., licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## What was changed from the original Roboto source

- Renamed family and internal font metadata to "Sky"
- Verified glyph construction against Sky's own design specification (see `docs/design/`) — a synthesis of Helvetica's structural discipline, Frutiger's aperture/ergonomic legibility, and Roboto's own screen-rendering engineering
- As of v0.1: measured analysis confirmed Roboto's x-height ratio (74.3% of cap-height), aperture openness on c/e (42–44°), R's leg angle, G's spur construction, the double-story a, and numeral (1/3/6) construction already meet or exceed the specification's targets — so v0.1 ships with no structural glyph edits beyond verification and rebranding
- From v0.5 onward, glyphs are being individually redrawn as original outlines — see `CHANGELOG.md` and `ROADMAP.md` for exactly which glyphs are original versus Roboto-derived at any given version

## Why this notice is this prominent

Apache 2.0 requires retaining the original copyright and license notice. We're also including this NOTICE.md as a standalone, linked-from-the-README document — not because the license requires that specific presentation, but because we think a project built on trust and legacy should make its lineage impossible to miss, not technically-compliant-but-buried.

Full license text: see [LICENSE](./LICENSE).
