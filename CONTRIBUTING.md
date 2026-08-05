# Contributing to Sky

Thank you for wanting to work on Sky. This document covers how to propose changes, what happens after you submit them, and where your effort is most valuable right now.

## Where help matters most right now

Sky's v0.1 foundation is verified but not original (see README). The single highest-value contribution today is **redrawing a glyph or glyph family** against the locked design spec in `docs/design/`, replacing the Roboto-derived outline with an original one. Check [ROADMAP.md](./ROADMAP.md) for the current milestone's target letters before starting — we sequence this deliberately (H/O/n first, since they set the DNA every other letter inherits from), so check that your intended glyph is actually next in line before investing time.

Other valuable contributions:
- **Kerning** — flagging or fixing specific letter-pair collisions
- **Documentation** — clarifying the design spec, fixing broken instructions, translating docs
- **Tooling** — build scripts, QA automation, website features
- **Bug reports** — rendering issues, missing glyphs, incorrect metrics

## Before you start a glyph redraw

1. Read the relevant section of `docs/design/` for that letter — every locked glyph has documented reasoning (design objective, optical theory, proportions, why alternatives were rejected). Your redraw needs to match the *spec*, not your own taste, unless you're proposing a spec change (see below).
2. Open an issue using the **Glyph Proposal** template before you start drawing, so two people don't duplicate the work and so a maintainer can flag anything the spec doesn't cover clearly.
3. Work in a branch named `glyph/{name}` — e.g. `glyph/lowercase-shoulder-family` if you're doing n/m/u/r together (recommended, since they share DNA and should stay visually consistent with each other).

## If you think the spec itself should change

Open an issue with the **Spec Change Proposal** template rather than just drawing it differently. Design decisions in Sky are documented with their reasoning specifically so they can be *challenged* with reasoning, not just overridden by whoever draws next. See [GOVERNANCE.md](./GOVERNANCE.md) for how these get decided.

## Submitting a PR

1. Make sure `sources/` is what you edited — never hand-edit files in `fonts/`, those are build outputs and will be overwritten
2. Run the local QA script (`scripts/qa.sh`) before pushing — it runs the same fontbakery checks CI will run
3. Fill out the PR template completely, including rendered proof at 12px, 16px, 24px, and 72px
4. A maintainer will review against the design spec, not personal preference — expect specific, spec-referenced feedback

## Code of Conduct

This project follows the [Code of Conduct](./CODE_OF_CONDUCT.md). Participation means agreeing to it.
