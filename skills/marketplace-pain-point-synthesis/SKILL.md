---
name: marketplace-pain-point-synthesis
description: Synthesize region-by-region or segment-by-segment research on a marketplace/collectibles-style product category into a small set of universal pain points (e.g. trust, liquidity, price discovery, access), each annotated with how it looks different per region, to find the "universal hook" that would work across otherwise very different markets. Use when asked to turn scattered regional/segment research into a small number of evidence-backed cross-market themes for a marketplace or collectibles product.
---

# Marketplace cross-market pain-point synthesis

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes the synthesis method used across Pokemon TCG regional research (Japan, China, North America, SEA, Korea, crypto/RWA layer) to marketplace and collectibles-adjacent products more broadly, where buying motivation and market structure differ sharply by region or segment but a smaller number of structural pain points recur everywhere.

## Procedure

1. **Gather region/segment-specific evidence separately first** — for each region or segment, document *why people buy* (motivation), what they trust, and what's broken, each claim tied to a source. Resist synthesizing across regions until each one is independently understood; premature synthesis flattens real differences (e.g. "financial product wearing a hobby costume" in one market vs. "cultural identity and craftsmanship" in another look nothing alike on the surface).

2. **Look for the same structural failure recurring under different surface descriptions.** A trust problem in one region might be "counterfeit physical goods," in another "wash trading with no oversight," in another "opaque custody" — these are the same underlying pain point (trust) with region-specific mechanics. Name the pain point at the level of abstraction where it recurs, not at the level of its most visible regional symptom.

3. **For each cross-market pain point, write one line per region/segment showing how it manifests there**, not a single generic description — the region-specific mechanic is what makes the synthesis credible and actionable (a generic "trust matters" is not useful; "SEA: physical counterfeits verified via in-person meetups; NA: wash trading with no regulatory oversight; JP: foreign scalpers exporting resealed boxes" is).

4. **Separate "real fragility" from "surface friction" per region.** Not every regional problem is equally load-bearing — flag which issue would actually break the market's trust/participation (e.g. counterfeits collapsing SEA's community trust layer) versus which is just an annoyance participants route around.

5. **State the universal hook**: the one capability that, if solved credibly, would work in every region/segment simultaneously even though the *reason* it matters differs by market. Justify it by showing it addresses the recurring structural pain point identified in step 2, not just by assertion.

6. **Flag where a solution optimized for one region/segment would lose another** — e.g. a product built purely around one region's dominant motivation (pure financial return) may fail in a region driven by a different motivation (cultural/collector identity). This keeps the universal hook honest about what it does and doesn't cover.

## Output shape

- Per-region/segment evidence notes: motivation → trust posture → what's broken, each cited.
- A short list (3-5) of cross-market pain points, each with one manifestation line per region/segment.
- Real-fragility vs. surface-friction flag per pain point per region.
- One stated universal hook, justified against the recurring pain point(s) it addresses.
