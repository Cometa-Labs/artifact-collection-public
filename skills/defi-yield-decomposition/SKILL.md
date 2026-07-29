---
name: defi-yield-decomposition
description: Decompose a headline DeFi/crypto yield (staking, lending, LP, LST) into its organic component (fees, MEV, staking rewards) versus its token-emission/incentive component, and flag what the yield looks like once emissions taper. Use when evaluating whether a quoted APY/APR is durable or propped up by a temporary incentive program.
---

Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

## When to use

You're evaluating a specific DeFi position's or protocol's headline yield (an LST, a lending market, an LP pool, a staking product) and need to know how much of it is real versus how much disappears when a token-incentive program ends.

## Procedure

1. **Identify every source contributing to the headline yield.** For crypto yield this typically decomposes into some subset of: trading fees, MEV capture, base protocol/staking rewards, and token emissions (governance/incentive tokens paid out on top of the base product).

2. **Classify each source as organic or emission-based.**
   - Organic: fees, MEV, staking rewards — these come from the protocol's actual economic activity and persist independent of any token-incentive program.
   - Emission-based: incentive tokens paid to depositors/LPs/borrowers to bootstrap usage. These are a subsidy, not economic activity, and are typically time-bounded or budget-bounded.

3. **Compute (or request, if the underlying data isn't available) the split** — what fraction of the headline yield is organic vs. emission-based. Where exact figures aren't available, state that the split is illustrative/approximate rather than presenting a precise-looking number with no real backing.

4. **State the "post-emission yield"** — what the yield would be with the emission component stripped out. This is the number to actually compare across competing products, since headline APY is not apples-to-apples when one product's yield is 80% emissions and another's is 80% organic.

5. **Flag emission-schedule risk explicitly.** Note whether the emission program has a known end date or taper schedule, and if so, that the yield will drop (sometimes sharply) at that point with no separate warning to depositors — this is the actual risk being surfaced, not just a footnote.

6. **Compare like-for-like across similar products** (e.g. multiple liquid staking tokens, or multiple lending markets for the same asset) using post-emission yield, not headline APY, to rank which is actually the better economic deal.

## Notes from the source example

- Products backed by the same underlying activity (e.g. multiple LSTs on the same chain) can have meaningfully different organic-vs-emission splits — one may capture MEV directly (higher organic yield) while another with no MEV capture leans more heavily on emissions to stay competitive on headline APY. Don't assume similar products have similar splits; check each one.
- A yield source that looks organic (e.g. "staking rewards") can itself be conditional — e.g. a position that exits a staking pool to enter a DeFi pool may forfeit staking rewards entirely unless the specific protocol is designed to preserve them. Verify whether the organic component survives the exact position structure being evaluated, not just the asset class in general.
