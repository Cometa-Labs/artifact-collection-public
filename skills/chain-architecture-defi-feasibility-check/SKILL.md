---
name: chain-architecture-defi-feasibility-check
description: Before proposing a DeFi strategy, agent workflow, or feature for a blockchain, check it against that chain's core architectural model (account-based vs UTXO/eUTxO, composability/mid-transaction contract calls, concurrency handling) to catch ideas that are infeasible by design rather than by missing tooling. Use when scoping DeFi or agent workflows for a specific chain, especially when porting an idea that worked on a different chain's architecture.
---

Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

## When to use

You're proposing a DeFi strategy, product feature, or AI agent workflow for a specific blockchain — especially one you're porting from experience on a different chain — and need to check whether the target chain's architecture actually supports it before scoping build effort.

## Procedure

1. **Identify the target chain's core execution model.** At minimum determine:
   - Account-based (state lives in persistent account balances, contracts can call other contracts mid-transaction) vs. UTXO/eUTxO-based (transactions consume and produce discrete outputs, inputs/outputs must typically be specified upfront).
   - Whether the chain supports composability — can one transaction call into multiple contracts and have later steps depend on the result of earlier ones within the same transaction (this is what enables flash loans, multi-step routing, and similar patterns).
   - How the chain handles concurrent access to the same contract/pool (e.g. does the model require batching or off-chain order aggregation because multiple users can't interact with the same contract state simultaneously).

2. **For each proposed strategy/workflow, ask whether it depends on a capability the architecture doesn't provide.** Common failure patterns:
   - Multi-step, same-transaction composability (e.g. flash loans, atomic multi-protocol routing) — infeasible on chains without mid-transaction contract-to-contract calls.
   - High-frequency simultaneous interaction with a single contract/pool (e.g. constant rebalancing against one pool by many users) — may require a batching/aggregation layer instead of direct interaction, changing both the UX and the latency characteristics.
   - Assuming uniform tooling across the ecosystem — wallet/interface behavior can vary significantly even within one chain's ecosystem (different wallet standards, some clients not supporting the relevant contract interactions at all), which affects whether a workflow can assume a consistent integration surface.

3. **If a strategy is architecturally blocked, don't scope it as "harder" — scope it as requiring a structurally different approach**, e.g. pre-computing and bundling inputs/outputs ahead of time instead of relying on runtime composability, or building against an off-chain aggregation/batching layer instead of raw contract calls. Flag this as deep, chain-specific engineering effort distinct from ordinary integration work.

4. **If a strategy is architecturally supported, still check what it changes about risk shape** — e.g. an account-based chain with shared collateral pools may have cross-position cascade risk that an isolated-margin design on another chain doesn't; composability that enables flash loans also enables new attack surfaces. Feasibility isn't just a green light — note the risk profile that comes with the architecture that permits the strategy.

## Notes from the source example

- The same class of strategy (e.g. an automated multi-step yield-routing agent) can be Tier-1 buildable on one chain and explicitly out of scope / high-effort on another purely because of the execution model — this isn't a resourcing gap, it's a design constraint that should be surfaced before a workflow gets prioritized alongside architecturally-simpler ones.
- When a chain's ecosystem lacks a capability other chains take for granted (e.g. deep native stablecoin liquidity, or flash loans), don't just note the gap — check what downstream strategies become correlated-risk or unavailable as a result (e.g. every yield strategy inherits the base asset's price risk if there's no deep stablecoin pairing).
