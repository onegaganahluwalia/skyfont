# Sky

**A typeface designed to disappear.**

Sky is an open-source sans-serif built for reading comfort first — quiet, calm, and legible at every size from a 12px UI label to a 72pt headline. It's built to be the font you install once and forget you're looking at.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-informational)](./CHANGELOG.md)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](./.github/workflows)

---

## Where Sky is right now — read this first

Sky is early, and we'd rather you know exactly what that means than find out later.

**v0.1 is a verified foundation, not yet an original typeface.** It's built on [Roboto](https://github.com/googlefonts/roboto)'s real, professionally-drawn outlines (Copyright Google Inc., Apache License 2.0), renamed and checked glyph-by-glyph against Sky's own design specification — a synthesis of Helvetica's structural discipline, Frutiger's ergonomic apertures, and Roboto's own screen-rendering engineering. That verification found Roboto's actual construction already meets or exceeds most of Sky's targets — which is a real, useful starting point, not a shortcut we're hiding.

**The roadmap from here is to make Sky fully original**, one glyph family at a time, hand-drawn against the locked design spec. See [ROADMAP.md](./ROADMAP.md) for exactly what "original" means at each version and when to expect it. Every release will be honest about how much of the font is redrawn versus inherited — that's not a policy, it's built into the version numbers themselves.

We think that's a more interesting story than pretending this started from nothing. If you're evaluating Sky for a project today, evaluate it as what it actually is: a rigorously verified, well-specified foundation with a concrete, public plan to become something original.

---

## Get Sky

| Format | Use case |
|---|---|
| [Download all weights (.zip)](./fonts/) | Desktop installation |
| `npm install @sky-type/sky` | Web projects |
| [Web font (CDN)](./docs/engineering/webfonts.md) | Drop-in `<link>` for websites |

Nine weights ship today: Thin, Light, Regular, Medium, Bold, Black, and Italic/Medium Italic/Bold Italic.

## Design philosophy

Read the full spec in [`docs/design/`](./docs/design/) — it covers metrics, aperture logic, terminal treatment, and every locked decision with the reasoning behind it, not just the numbers. Short version: nothing in Sky should call attention to itself. Every choice optimizes for the reader forgetting they're reading a typeface at all.

## Contributing

Sky is a community project from day one — see [CONTRIBUTING.md](./CONTRIBUTING.md) for how glyph proposals, kerning fixes, and documentation improvements get reviewed and merged. The most valuable contribution right now is exactly what the roadmap needs: hand-drawn glyphs replacing the Roboto-derived foundation, one letter family at a time.

## Governance

See [GOVERNANCE.md](./GOVERNANCE.md) for how design decisions get made and who can make them.

## License

Apache License 2.0 — see [LICENSE](./LICENSE) and [NOTICE.md](./NOTICE.md) for full attribution to Roboto, as required by license terms.
