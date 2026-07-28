---
name: marketplace-competitor-quadrant-mapping
description: Map a marketplace or collectibles-adjacent competitive landscape by scoring every competitor on a shared set of bipolar dimensions (e.g. custody credibility, liquidity guarantee, accessibility), categorizing them by business model, then plotting dimension pairs as quadrants to find empty/underserved positioning space. Use when asked to build a competitor map, positioning matrix, or "whitespace" analysis for a marketplace, RWA/tokenization, or collectibles-style product.
---

# Marketplace competitor quadrant mapping

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes the competitor-mapping method used for Pokemon TCG/collectibles platforms (Courtyard, Whatnot, Fanatics Collect, Alt, TCGplayer, etc.) to marketplace-style and collectibles-adjacent products more broadly: any space with multiple platforms competing on trust, liquidity, accessibility, and financial sophistication rather than a single obvious axis like price.

## Procedure

1. **Define 6-10 bipolar dimensions** that matter for this category, each with a concrete low pole and high pole (not just a label). E.g. "Custody Credibility: No custody (seller holds item) ↔ Institutional-grade (named vault, audit, insurance)." A dimension without both poles clearly defined can't be scored consistently across competitors — write the poles before scoring anyone.

2. **Group competitors into categories by business model**, not by size or brand — e.g. RWA/crypto-native, live/entertainment commerce, traditional marketplace, emerging/early-stage, institutional investment product. The category becomes the plot's color/shape encoding later, and it's often more explanatory than any single dimension score.

3. **Score every competitor on every dimension (1-10)**, sourced from direct product research (site navigation, actual UI, pricing pages, disclosed scale metrics) rather than marketing copy alone. Where a site can't be scraped directly, say so explicitly and note the score is inferred from secondary sources — don't silently treat inferred and directly-observed scores as equal-confidence.

4. **Write one evidence note per dimension per competitor**, not just the number — the note is what makes the score defensible and reusable later (e.g. "90% instant buyback on every vending machine pull" backs a liquidity score of 9). A score with no note is close to worthless for anyone auditing it later.

5. **Choose 2-3 dimension pairs to plot as quadrants**, prioritizing pairs where you suspect a market gap over pairs that just confirm the obvious. For each plot, state the insight in one sentence: which quadrant is crowded, which is empty, and why that emptiness is a positioning opportunity rather than a sign nobody wants it (distinguish "no one has built this" from "this was tried and failed" using the evidence you gathered).

6. **State the primary recommended plot** — the single dimension pair that most directly answers "where's the whitespace" — separately from the other supporting plots, so the reader isn't left to guess which chart matters most.

## Output shape

- Dimension definition table: # → dimension → low pole → high pole.
- Competitor score matrix: one row per competitor, one column per dimension, plus category.
- 2-3 quadrant plots (dimension pair, axis labels, one-sentence insight each), with one flagged as primary.
- Evidence notes per competitor per dimension, kept alongside the score, not discarded after plotting.
