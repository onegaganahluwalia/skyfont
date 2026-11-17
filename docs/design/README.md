# Sky Design Specification

This is the authoritative design spec Sky's glyphs are built and verified against. Every locked number here traces back to a stated reason — if you're proposing a change, engage with the reasoning, not just the number (see [Spec Change Proposal](../../.github/ISSUE_TEMPLATE/spec_change.md)).

## What this typeface is trying to be

Synthesize the three most successful sans-serifs of the last century: **Helvetica's** architectural neutrality and stroke discipline, **Frutiger's** open apertures and ergonomic warmth (originally engineered for reading at a distance and in motion — airport signage), and **Roboto's** screen-native engineering discipline — built to survive hinting, subpixel rendering, and a fragmented global device fleet. The goal isn't novelty. It's a typeface resolved enough on every fundamental that it becomes the default choice — invisible, elegant, and functionally correct from a notification badge to a headline.

| Source | What it contributes |
|---|---|
| Helvetica | Skeletal neutrality and authority. No stroke exists that isn't structurally necessary. |
| Frutiger | Open apertures and ergonomic legibility — proof a grotesque skeleton can stay open without losing authority. |
| Roboto | Screen-rendering engineering discipline — works under hostile rendering conditions, not just in a specimen PDF. |

## 1. Skeletal Proportions & Metrics (actual measured values, locked)

| Metric | Value | Notes |
|---|---|---|
| UPM | 2048 | — |
| Cap height | 1456 units | Flat-top reference (H) |
| **X-height** | **990 units (68.0% of cap)** | **Sky's defining proportion — deliberately classical, quieter than Roboto's ~74%** |
| Ascender | 1536 units | b, d, h, k, l — flat top, no overshoot |
| Descender | −427 units | g, p, q, y, j |
| Default line-height | 1.45× | Baked into typo ascender/descender, not lineGap |
| Digit width (tabular) | 1114 units | All 10 digits equal |
| Overshoot top (O,o,c,e,s,S,C,G,Q) | +17–20 units | Proportional to cap height |
| Overshoot bottom (O,o,c,e,s,S,C,G,Q,0) | −20 units | Pre-existing from Roboto foundation, retained |
| Advance width vs Roboto | ~3.2% narrower | Side-bearing led — letterforms not compressed |



**x-height:** 68.0% of cap-height (990 / 1456 units). *(Locked and verified: applied in v0.1 via per-weight outline scaling. OS/2 `sxHeight` confirmed at 990 across all 9 fonts as of v0.2. This is Sky's defining proportion — deliberately lower than Roboto's ~74% and Helvetica's ~71%, giving text a classical, quieter presence.)*

**Stem-to-counter ratio:** Regular weight stems at ~12% of cap-height. *(Verified: measured at 175u / 1456u = 12.0% on the H glyph. Family progression: Thin 2.5% → Light 7.2% → Regular 12.0% → Medium 16.1% → Bold 19.4% → Black 22.9%. Progression is smooth and monotonic.)*

**Overall width — deliberate design choice, not a compliance fix:** Sky ships ~3.2% narrower than its Roboto foundation, measured on a full sentence at real text size. This comes entirely from proportionally tighter side-bearings (12% reduction, scaled to each glyph's own natural spacing) applied uniformly across the whole family — never from compressing letterforms, which would distort curves and risk clogging counters. Verified with zero letter-collision risk across tight combinations (e.g. "illwork mrnvvw") before shipping. This is a stated preference for a quieter, more restrained reading rhythm, not a correction of an error — Roboto's original spacing was already correct for its own purposes.

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

## 3a. O / o — curve DNA (v0.5, letter #2)

**Status: geometry repaired, curve character unchanged from the foundation. Tension is an open decision (see below).** The design spec never defined numeric targets for O (stress, contrast, superellipse), so this section records what was *measured*, what was wrong, and what was changed. The numbers in §1 predate the v0.3 −12% condensing; the values below are measured on the condensed v0.3 files.

**What was wrong (measured on v0.3.0, Regular):** the v0.2 x-height scaling (y-zone 0–1082 → 0–990) leaked into the capital O, and the overshoot re-correction later moved only the *top* of o.

| | O top | O bottom | O lower vs upper squareness | o top | o bottom |
|---|---|---|---|---|---|
| Roboto foundation (uncondensed) | 164u | 163u | symmetric | 152u | 152u |
| Sky v0.3.0 | 164u | **148u** | lower bowl squarer (0.15 vs −0.03…0.11), upper-left ≠ upper-right handles | **154u** | 139u |
| Sky v0.5 (this change) | 164u | 163u | symmetric (0.10 / 0.10 / 0.10 / 0.11) | 139u | 139u |

A bottom stroke ~10% lighter than the top, and a lower bowl drawn tighter than the upper, are both the opposite of standard optical practice: round letters should sit at least as heavy at the baseline as at the top. All nine styles showed the same pattern (Bold O 248/224, Black 275/248; o top-heavy by 8–17u in every style).

**What changed (O and o only, all 9 styles):** each glyph was rebuilt from its own-weight Roboto v2.138 outline using only the documented family transforms, as one exact affine map per glyph — x scaled ≈ 0.88 so the outline lands on the current v0.3 bounds (advance widths and side bearings unchanged, ±1u on MediumItalic o), y untouched for O (already −20 / 1476), y × 0.915 for o (−20 / 1007, the locked 990 + 17 overshoot). Script: `scripts/glyphs/rebuild_O_o.py`.

**Measured after (stroke thickness in font units; squareness 0 = ellipse, 1 = rectangle, outer contour):**

| Style | O side | O top/bottom | O squareness | o side | o top/bottom | o squareness | O adv ÷ H adv |
|---|---|---|---|---|---|---|---|
| Thin | 48 | 54 / 54 | 0.13 | 47 | 49 / 49 | 0.07 | 0.958 |
| Light | 108 | 108 / 108 | 0.12 | 106 | 93 / 93 | 0.07 | 0.966 |
| Regular | 168 | 164 / 163 | 0.10 | 164 | 139 / 139 | 0.06 | 0.972 |
| Medium | 223 | 209 / 208 | 0.09 | 214 | 178 / 178 | 0.07 | 0.978 |
| Bold | 268 | 248 / 247 | 0.09 | 255 | 213 / 213 | 0.08 | 0.985 |
| Black | 314 | 275 / 274 | 0.08 | 297 | 238 / 238 | 0.09 | 0.990 |
| Italic | 164 | 159 / 158 | — | 158 | 136 / 135 | — | 0.955 |
| Medium Italic | 217 | 203 / 201 | — | 207 | 174 / 173 | — | 0.960 |
| Bold Italic | 261 | 240 / 239 | — | 247 | 208 / 207 | — | 0.952 |

Vertical stress throughout (thickest at 3 and 9 o'clock in uprights). Overshoot locks verified: O −20 / +1476, o −20 / +1007 (italics −20 / +1006, as before). Outline QA: 2 contours, outer clockwise / inner counter-clockwise, no overlaps, points on extrema in uprights, max rounding kink 0.9° (italics; v0.3 had up to 2.4°). Uprights Thin–Bold now share one 28-point structure for O and o (Black O: 26), which helps the future v2.0 variable font.

**Not yet decided — curve tension.** v0.5 keeps the foundation's squareness (O ≈ 0.10, o ≈ 0.06–0.09 in Regular). A squarer "+0.12 tension" alternative (O ≈ 0.21, o ≈ 0.18) was proofed but **not** applied; choosing it would be a spec decision and should go through a Spec Change Proposal.

**Known side effects / follow-ups:**
- c, e, s still carry the top-heavy pattern (Regular top 154 / bottom 139); C, G, Q, D, U, S, 0, 3, 8 still carry the thinned bottom strokes; Ø/ø/Œ/œ are separate outlines still on the old O/o. They should inherit this fix when their turn comes.
- The same v0.2 zone leak lowered and thinned cap crossbars (Regular H bar 673–830 → 605–746, 157u → 141u; E, F, B, P, R, A likewise). This is a family-wide issue, not an O issue.

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
