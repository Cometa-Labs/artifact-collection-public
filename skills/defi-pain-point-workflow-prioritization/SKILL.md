---
name: defi-pain-point-workflow-prioritization
description: Turn sourced user pain points for a crypto/DeFi protocol ecosystem into a ranked list of candidate AI agent (or feature) workflows, scored on user value vs build feasibility. Use when scoping what to build for a DeFi ecosystem and you need to go from "users are frustrated by X" to a prioritized, tiered build list.
---

Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

## When to use

You're scoping product/agent opportunities for a crypto or DeFi protocol ecosystem (a chain, a category of protocols, or a single protocol) and need to move from scattered user complaints to a small, defensible, ranked build list — not just a feature wishlist.

## Procedure

1. **Source pain points from primary evidence, not speculation.** Pull from: protocol documentation (especially weakness/limitations sections), ecosystem analysis reports, founder/team public statements, and forum/community posts. Each pain point must trace to at least one of these sources — don't invent pain points from general intuition about what "should" be annoying.

2. **Give each pain point a short ID and a one-line description** naming which protocol(s) or part of the ecosystem it hits and why it happens mechanically (not just "users are confused" — state the mechanism, e.g. "LST collateral depegs 2-3% under stress, no automated alerts").

3. **Score each pain point on two axes:**
   - **Severity** — how bad the pain is when it happens (e.g. lost funds vs. minor friction).
   - **Frequency** — how often users actually hit it.
   Don't collapse these into one number yet; keep them separate so a rare-but-catastrophic pain point (e.g. liquidation risk) doesn't get diluted by a common-but-minor one (e.g. UI inconsistency).

4. **For each pain point (or cluster of related pain points), propose a candidate workflow** — a concrete agent or feature that would address it. Name which pain point ID(s) it addresses; a workflow addressing multiple related pain points is stronger than several narrow ones.

5. **Score each candidate workflow on two axes:**
   - **User value** = a function of the severity × frequency of the pain point(s) it addresses. Higher severity+frequency pain points justify building the workflow even if it's harder.
   - **Build feasibility** = API/data availability, technical complexity, and regulatory/custody risk (a workflow that needs pre-authorized fund movement is lower feasibility than a read-only monitor, regardless of user value).

6. **Plot workflows on a 2x2 (user value × build feasibility) and bucket into tiers:**
   - **Tier 1 (build first)**: high value, high feasibility.
   - **Tier 2 (medium priority)**: high value but harder to build, or easier but lower value.
   - **Tier 3 (lower feasibility / high risk)**: valuable in theory but blocked by custody risk, missing infrastructure, or deep domain-specific engineering (e.g. anything requiring pre-authorized fund movement, or deep protocol-specific transaction batching).

7. **State the top-tier picks explicitly** — don't leave the ranking implicit in a table. Call out which workflows you'd build first and why, referencing the specific pain point IDs each one clears.

## Notes from the source example

- Different sub-ecosystems within the same chain-pair comparison can call for structurally different agent strategies (e.g. a "sophistication layer" — aggregate/optimize across protocols that already work — vs. an "activation layer" — lower the barrier for users who haven't engaged at all). Name which strategy pattern a given ecosystem needs before generating workflow candidates; it changes what "high value" means.
- Workflows that require executing transactions on a user's behalf (vs. monitoring/alerting/suggesting) should be scored lower on feasibility by default and flagged as needing explicit pre-authorization design, regardless of how well they score on user value.
