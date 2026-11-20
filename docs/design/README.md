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

**Status: geometry repaired and curve tension set by an approved spec change (option B, below).** The design spec never defined numeric targets for O (stress, contrast, superellipse), so this section records what was *measured*, what was wrong, and what was changed. The numbers in §1 predate the v0.3 −12% condensing; the values below are measured on the condensed files.

**What was wrong (measured on v0.3.0, Regular):** the v0.2 x-height scaling (every point with 0 < y ≤ ~1104 multiplied by 0.898 = 990/1102, see §3b) leaked into the capital O, and the overshoot re-correction later moved only the *top* of o.

| | O top | O bottom | O lower vs upper squareness | o top | o bottom |
|---|---|---|---|---|---|
| Roboto foundation (uncondensed) | 164u | 163u | symmetric | 152u | 152u |
| Sky v0.3.0 | 164u | **148u** | lower bowl squarer (0.15 vs −0.03…0.11), upper-left ≠ upper-right handles | **154u** | 139u |
| Sky v0.4.0 | 164u | 163u | symmetric | 139u | 139u |

A bottom stroke ~10% lighter than the top, and a lower bowl drawn tighter than the upper, are both the opposite of standard optical practice: round letters should sit at least as heavy at the baseline as at the top. All nine styles showed the same pattern (Bold O 248/224, Black 275/248; o top-heavy by 8–17u in every style).

**Geometry (O and o only, all 9 styles):** each glyph is rebuilt from its own-weight Roboto v2.138 outline using only the documented family transforms, as one exact affine map per glyph — x scaled ≈ 0.88 so the outline lands on the v0.3 bounds (advance widths and side bearings unchanged), y untouched for O (already −20 / 1476), y × 0.915 for o (−20 / 1007, the locked 990 + 17 overshoot). Script: `scripts/glyphs/rebuild_O_o.py`.

### Spec change — curve tension (option B), approved by Gagan on 18 Nov 2026

The foundation O/o were Roboto-round (Regular squareness O ≈ 0.10, o ≈ 0.06). **Approved spec change, approved by Gagan on 18 Nov 2026: Sky's O/o take the squarer, Helvetica-leaning curve ("option B", about +0.12 tension).** This is the curve DNA the other round letters inherit.

- **Method.** For every curve arc between two on-curve points, the arc's corner is the intersection of its two end tangents (the extremum tangents). Every off-curve point slides toward that corner by a fraction *t*. End tangents don't change, so curves stay smooth and extrema stay on extrema; stroke thickness at 12/3/6/9 o'clock is unchanged. The construction is affine-invariant, so it means the same thing on slanted outlines.
- **Uprights:** *t* = 0.12 in all six weights.
- **Italics — derived consistently, not copied.** Roboto's italic O/o are drawn slanted with 3 off-curve points per quarter (not 2), so the upright *t* doesn't transfer literally. Each italic gets the *t* that gives its de-slanted (8.66°) outer contour the same mean squareness as its upright partner: Italic O 0.148 / o 0.141, Medium Italic 0.149 / 0.145, Bold Italic 0.148 / 0.147 (`scripts/glyphs/o_tension.json`). Roboto's italic O is deliberately squarer on the top-right / bottom-left diagonal than on the other one (−0.01…0.02 vs 0.14 before tension). That diagonal character is kept; only the overall squareness is matched.

**Measured after (stroke thickness in font units; squareness 0 = ellipse, 1 = rectangle, outer contour on the bbox diagonal, italics measured de-slanted by 8.66°):**

| Style | O side | O top/bottom | O squareness | o side | o top/bottom | o squareness | O adv ÷ H adv |
|---|---|---|---|---|---|---|---|
| Thin | 48 | 54 / 54 | 0.24 | 47 | 49 / 49 | 0.18 | 0.958 |
| Light | 108 | 108 / 108 | 0.22 | 106 | 93 / 93 | 0.18 | 0.966 |
| Regular | 168 | 164 / 163 | 0.21 | 164 | 139 / 139 | 0.18 | 0.972 |
| Medium | 223 | 209 / 208 | 0.20 | 214 | 178 / 178 | 0.18 | 0.978 |
| Bold | 268 | 248 / 247 | 0.20 | 255 | 213 / 213 | 0.19 | 0.985 |
| Black | 314 | 275 / 274 | 0.19 | 297 | 238 / 238 | 0.20 | 0.990 |
| Italic | 164 | 162 / 161 | 0.21 | 159 | 138 / 138 | 0.17 | 0.955 |
| Medium Italic | 217 | 207 / 206 | 0.20 | 208 | 177 / 177 | 0.18 | 0.960 |
| Bold Italic | 262 | 246 / 245 | 0.20 | 249 | 211 / 211 | 0.19 | 0.952 |

Vertical stress throughout. Overshoot locks verified: O −20 / +1476, o −20 / +1007 (italics −20 / +1006). Outline QA: 2 contours, outer clockwise / inner counter-clockwise, no overlaps, no new kinks.

**Known follow-ups:**
- Ø/ø/Œ/œ and the C, G, Q, D cap rounds are separate outlines. They are now geometrically repaired (§3b) but still carry Roboto's rounder curve, not the approved tension. They should inherit it when their turn comes.
- c, e, s are still top-heavy (Regular c/e/s top ≈ 154 / bottom ≈ 139). That is lowercase-zone work, queued as c and s in the roadmap.

## 3b. Family repair — undoing the v0.2 x-height scaling where it never belonged (v0.4)

**What happened in v0.2 (reconstructed by measurement, all 9 styles):** to lower the x-height to 990, *every* point with 0 < y ≤ ~1104 was multiplied by k = 0.8983 (= 990/1102; italics 0.8967 / 0.8967 / 0.8952, and the zone top is ~1106–1110 there). Points above that line and below the baseline were left alone, and x was never touched. That is right for lowercase, but it also hit every capital, figure and cap-height symbol, squashing their lower ~75% while their tops stayed put:

| Regular, horizontal-stroke edges on a vertical cut | v0.3.0 | v0.4.0 | Roboto v2.138 target |
|---|---|---|---|
| H crossbar | 605–746 (141u) | 673–830 (157u) | 673–830 |
| E bottom / middle bar | 0–141 / 605–746 | 0–157 / 673–830 | 0–157 / 673–830 |
| F bar | 578–720 | 643–801 | 643–801 |
| A bar | 342–484 | 381–539 | 381–539 |
| B middle junction | 612–751 | 681–836 | 681–836 |
| P / R bowl bottom | 513–654 / 530–671 | 571–728 / 590–747 | 571–728 / 590–747 |
| C / Q / U bottom-stroke thickness | 143 / 148 / 143u | 158 / 163 / 157u | 158 / 163 / 157u |
| S / 3 middle spine | 581–749 / 598–737 | 647–831 / 666–820 | 647–833 / 666–820 |
| 0 / 3 bottom-stroke thickness | 139 / 139u | 152 / 152u | 152 / 152u |
| Bold H bar / A bar | 561–778 / 270–488 | 624–866 / 300–543 | 624–866 / 300–543 |

In the italics the zone boundary also **kinked every stem** that crosses it: segments below the line leaned 9.6°, above it 7.5° (H, E, B, D, P, R, 1, 4 …). After the repair every straight stem leans 8.6–8.7°.

**Detection (per glyph, per style, by measurement — `scripts/glyphs/repair_v02_zone.py`):** each simple glyph's points between the baseline and the zone top are compared with the same-named Roboto glyph of the same weight. A glyph is *squashed* when most of those points match k·y_Roboto rather than y_Roboto. The scope rule, which is what separates "x-height design" from "cap-height design":

- **Restored:** uppercase in every script (Latin, Greek, Cyrillic, Coptic-in-Latin, IPA caps), the `.ss06` cap alternates, lining figures (default and proportional), Nl (Roman numerals), currency, plus punctuation, symbols and modifier/superscript letters whose Roboto design reaches cap height (yMax ≥ 1300: quotes, ! ? & @ # % ‰ § ¶ © ® ™ † ‡ ( ) [ ] { } ⁄ and the superscripts and modifier letters).
- **Kept as v0.2 made them:** lowercase and their small-cap / unicase / old-style / numerator / denominator forms (x-height or fraction system; dnom standardised in v0.2); combining marks; punctuation and symbols that sit below cap height (period, comma, colon, hyphen, guillemets, math operators — x-height-relative); titlecase digraphs (Dž etc., part cap and part lowercase — flagged, not touched); O/o (§3a).

| Style | Glyphs restored | of which uppercase / figures / other |
|---|---|---|
| Thin | 516 | 259 / 10 / 247 |
| Light | 522 | 259 / 10 / 253 |
| Regular | 527 | 259 / 10 / 258 |
| Medium | 528 | 260 / 10 / 258 |
| Bold | 530 | 261 / 10 / 259 |
| Black | 533 | 261 / 10 / 262 |
| Italic | 526 | 259 / 10 / 257 |
| Medium Italic | 528 | 260 / 10 / 258 |
| Bold Italic | 530 | 261 / 10 / 259 |

The counts differ slightly by weight because detection is by measurement: e.g. the quotes and ˚ sit entirely above the zone in Thin (nothing to undo), but dip into it in heavier weights. About 480–490 composites per style (Á, Ĥ, Ǻ, Ё …) inherit the fix automatically through their component references.

**Restore method — Roboto v2.138 per-weight outlines + the documented family transforms.** The squash touched y only, so the target "Roboto outline, condensed and spaced as Sky, with Sky's own modifications" is reached exactly by inverting it on the Sky outline: y = y_sky / k inside the zone, then snap each point to the Roboto y of the same glyph when within 2.5u (removes v0.2 rounding). That keeps Sky's x (−12% condensing, spacing, advance widths, kerning — all byte-identical) and keeps every modification Sky made on top:

- **Corner-softening re-applied and verified.** Every orthogonal corner on E F H I L T (and the stems of B D P R) is again a 2-point chamfer of 9u in y (8u in x after condensing). v0.3 had 8u chamfers below the zone line and 9u above. Regular: 92 / 92 chamfers at 9u; all styles 52 / 52 on E F H I L T B D P R. The H (verified modification) keeps its outline structure; only its bar moved back up and regained its weight.
- **Sky's deliberate edits preserved.** Wherever Sky had moved a point away from Roboto (C terminal cut, the 2's foot, a few italic U points…), that offset is kept.
- **Guard:** a structure-independent check — the mean distance from the Sky outline to the x-fitted Roboto outline — must improve, or the glyph is left alone. Result: mean distance 13–20u before → 0.17–0.20u after in every style; 0 glyphs reverted.

**Outline QA (every changed glyph):** no contour-direction changes, no new overlaps, no new kinks in the main set. The worst remaining new kinks are 2–4.5° rounding bends in rare symbols (§, ⸾, uniFFFD); 3 italic modifier letters (U+1D61, U+1D4E, U+A71D) gained a 1.7–1.9u off-extremum control point.

## 3c. Italic angle (v0.4)

Sky's italics declared Roboto's nominal angle: `post.italicAngle` −12° with an hhea caret of 100/21 (11.9°). But that is not the slant of the outlines. Roboto's own stems lean 9.86°, and the v0.3 −12% condensing reduced that to atan(0.88 · tan 9.86°) = 8.68°. **Measured on the repaired outlines** (median over the straight stems of I l H T E L F h d b): Italic 8.659°, Medium Italic 8.649°, Bold Italic 8.659°.

- **Now:** `post.italicAngle` = **−8.66°** in all three italics. hhea caret = 2048 / 312 (= 8.66°). fontbakery `caret_slope` goes from WARN to PASS.
- An earlier note estimated "≈10.6°" by assuming Roboto's true slant was 12°. That was wrong; the measured value above replaces it.

## 3d. Side-bearing metadata (v0.4)

In v0.3, ~1,300–1,440 glyphs per font (almost all accented composites, plus A V W X Y v w x, whose corner-softening moved xMin) had an hmtx left side bearing that disagreed with the outline's xMin, typically by 2–18u. The outlines already render in the right place in Chrome and unhinted FreeType (checked). This is a metadata fix: lsb now equals xMin for every glyph. It matters for anything that positions from hmtx / phantom points (TrueType hinting, some PDF and layout tools). Advance widths unchanged. Script: `scripts/fix_metrics.py`.

**Accent spacing (v0.4, fixed):** composites' advance widths didn't match their base letters. In v0.3 the base letters were re-spaced but composites only kept Roboto × 0.88, so É was 35u wider than E and á 23u wider than a in Regular. Now every letter+marks composite takes its base's advance (plus Roboto's own deliberate extra, condensed, where Roboto widens: ď ľ ť, Greek tonos). Each mark sits where Roboto puts it relative to the base (median error 0.3u). Script: `scripts/glyphs/fix_composite_spacing.py`.

## 3e. Round capitals inherit the O curve (v0.4)

C, G, D and Œ take the same tension operator as O, at the style's O value. Q and Ø are rebuilt on the new O with their own tail / slash. Measured squareness (Regular, outer contour, per quadrant UR/UL/LL/LR): C 0.23/0.10/0.10/0.23 → 0.31/0.21/0.21/0.30; G 0.26/0.12/0.07/0.44 → 0.32/0.23/0.18/0.47; Œ bowl 0.32 → 0.40; the D bowl corners 0.01 → 0.12; Q bowl 0.16 → 0.26. Straight parts, terminals and stroke weights are unchanged.

## 3f. Low punctuation (v0.4)

Period, comma, „ and ‚ were ~10% flat from the v0.2 scaling (Regular period 189u vs Roboto's 210u). They are restored to Roboto's shape on the baseline. ·, • and the dots of ¡ ¿ are restored about their own centres. The colon/semicolon upper dot offset had never been scaled with the x-height and sat 82u above it; it now gets the same y × 0.898 (+ italic slant) as the outlines and tops out at the x-height. Script: `scripts/glyphs/restore_low_punct.py`.

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
