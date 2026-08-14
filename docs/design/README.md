# Sky Design Specification

This is the authoritative design spec Sky's glyphs are built and verified against. Every locked number here traces back to a stated reason — if you're proposing a change, engage with the reasoning, not just the number (see [Spec Change Proposal](../../.github/ISSUE_TEMPLATE/spec_change.md)).

## What this typeface is trying to be

Synthesize the three most successful sans-serifs of the last century: **Helvetica's** architectural neutrality and stroke discipline, **Frutiger's** open apertures and ergonomic warmth (originally engineered for reading at a distance and in motion — airport signage), and **Roboto's** screen-native engineering discipline — built to survive hinting, subpixel rendering, and a fragmented global device fleet. The goal isn't novelty. It's a typeface resolved enough on every fundamental that it becomes the default choice — invisible, elegant, and functionally correct from a notification badge to a headline.

| Source | What it contributes |
|---|---|
| Helvetica | Skeletal neutrality and authority. No stroke exists that isn't structurally necessary. |
| Frutiger | Open apertures and ergonomic legibility — proof a grotesque skeleton can stay open without losing authority. |
| Roboto | Screen-rendering engineering discipline — works under hostile rendering conditions, not just in a specimen PDF. |

## 1. Skeletal Proportions & Metrics

**x-height:** 73% of cap-height. *(Verified: Sky's Roboto-derived foundation measures 74.3% — already within target, no adjustment needed for v0.1.)*

**Stem-to-counter ratio:** Regular weight stems at 9.5–10% of cap-height as an initial target. *(Verified: Roboto's actual stems measure ~13.3% of cap-height — heavier than this original estimate. Decision: keep Roboto's proven, real-world-tested weight rather than thin it based on a desk estimate. This spec value is retained here for historical reasoning; treat 13.3% as the current working target until a deliberate decision changes it.)*

**Aperture openness (c, e, s):** the highest-leverage decision for small-size legibility.

| Letter | Target | Verified (v0.1) |
|---|---|---|
| c | ~34–36° open, centered at 3 o'clock | 43.9° — exceeds target |
| e | ~12–15% wider than Helvetica's | ~42° gap measured — exceeds target |
| s | Widest aperture budget of the three (double-curve structure clogs first) | Not yet individually re-measured; treat as provisionally compliant pending a dedicated check |

## 2. Terminal Cuts, Junctions & Optical Corrections

**Terminal cuts:** 3–6° off true horizontal/vertical, in the direction the stroke is moving. Pure Helvetica-style perpendicular cuts read cold under sustained reading; pure calligraphic angles undercut structural authority. Exception: strokes terminating flush at the baseline (like R's leg) get a horizontal cut regardless of the stroke's own angle — this is standard practice, not a deviation.

**Junctions (stem meets bowl — P, R, b, d, p, q):**
- Micro ink-traps: 2–4% of stem width, notched into the inside of the junction — invisible at reading size, prevents fill-in at small sizes or low pixel density
- Weight easing: bowl stroke thins 4–6% immediately adjacent to the stem junction, compensating for optical mass-doubling where straight and curved strokes overlap

## 3. Critical Glyph Anatomy

| Glyph | Construction | Verified (v0.1) |
|---|---|---|
| **R** (leg) | Straight (not curved), 31–34° from vertical, launching at ~60% of cap-height | Visually confirmed close to target |
| **G** (spur) | Short, straight internal spur closing 60–65% of the counter, near-tangent join (not perpendicular) | Visually confirmed close to target |
| **a** | Double-story, grotesque-derived, with humanist bowl loosening (~4–5% wider than strict grotesque) | Double-story construction confirmed |
| **1** | Flag at top-left, soft-angle cut, no base serif | Confirmed present |
| **3** | Flat-ish top curve (not fully round), upper bowl slightly smaller than lower | Confirmed close to target |
| **6** | Open counter, standard junction easing, no spur | Confirmed |

## 4. Optical Sizing & Weight Matrix

A single master can't serve both a 12px UI label and a 72pt headline — this table is the reasoning for why sizes need to diverge from the Text baseline, not just a style guide.

| Range | Contrast | Stem thickness | Apertures | Tracking |
|---|---|---|---|---|
| Micro/UI (10–14px) | Near-zero | +8–10% heavier than Text | +6–8% more open than base spec | +15–20 units looser |
| Text (9–14pt) | Base spec | Base spec | Base spec | Base spacing (reference point) |
| Subhead (18–36pt) | +5–8% thick/thin contrast | −3–4% lighter | Slightly tighter than base | Eases toward −5 units |
| Display (48–72pt+) | Full contrast, 12–15% | −8–10% lighter | Can close toward precise geometry | −15–20 units tighter |

**Screen-rendering discipline (Roboto's specific contribution):** stems should snap to whole-pixel boundaries at common UI sizes (14–16px); diagonal strokes (v, w, x, y, k) need their own hinting instructions rather than inheriting stem logic; no optical correction is signed off from the vector outline alone — always check at actual rendered pixel sizes (12px, 14px, 16px minimum).

---

**On the "Verified" column above:** these are the actual measurements taken against Sky's v0.1 Roboto-derived foundation, documented plainly rather than assumed. Where a value hasn't been individually re-checked, this doc says so — that's the same honesty principle the rest of the project runs on.
