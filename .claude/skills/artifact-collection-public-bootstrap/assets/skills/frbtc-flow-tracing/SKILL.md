---
name: frbtc-flow-tracing
description: Trace a chain of frBTC wrap/swap/unwrap/deferred-dispatch transactions on Bitcoin (via the wdsx7 protocol and an Alkanes AMM) to compute net BTC flow, compare expected vs actual payouts, and surface undisclosed fees. Use when auditing an address's wrap/unwrap transaction history, verifying a protocol's "no fees" claim against on-chain data, or explaining why a user's BTC balance dropped across a wrap → swap → unwrap round trip.
---

# frBTC wrap/unwrap flow tracing

> Auto-generated from open-domain document content (a single worked transaction trace) and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows. Treat the procedure below as a starting point to verify against current protocol behavior, not as ground truth.

This skill generalizes a worked example: an 8-transaction trace on a single Bitcoin address that wraps BTC into frBTC, swaps it for a paired asset (DIESEL) and back, unwraps, and receives a deferred payout from the wdsx7 protocol's dispatch mechanism. The goal each time is the same — reconcile what a user actually received against what the protocol's own numbers say they should have received, and attribute every satoshi of the difference to a named cause.

## When a transaction chain fits this pattern

Look for this sequence of opcodes/behaviors on an address:

1. **Wrap** (`frBTC Wrap`, e.g. opcode 77): user BTC input splits into an AMM carrier UTXO + a `wdsx7 reserve` locked UTXO + user change. frBTC is minted 1:1-ish against the locked reserve, minus a small withheld amount (the wrap fee).
2. **AMM swap(s)**: frBTC trades against a paired token through an AMM carrier UTXO. The AMM keeps a fee; the user's remaining frBTC/BTC carries forward to the next TX.
3. **Unwrap** (`frBTC Unwrap`, e.g. opcode 78): the frBTC carrier is burned. Critically, **wdsx7 does not appear as an input on the unwrap TX itself** — the unwrap just closes out the user's carrier UTXOs and burns the frBTC. A flat dust fee (e.g. 546 sats) typically goes to wdsx7 here.
4. **Deferred dispatch**: several blocks later (observed: ~8-10 blocks), wdsx7 issues the actual BTC payout in a **separate batch transaction** that also services other users' unwraps in the same TX. This is where the reserve locked back in step 1 actually gets released.

If you see wrap → (swap →)* unwrap, with no payout in the unwrap TX itself, expect a corresponding dispatch TX later from the same protocol address — go find it before concluding anything about what the user received.

## Procedure

1. **List every TX for the address in order**, noting confirmations (higher confirmations = older). Classify each one by which of the four behaviors above it matches, using its inputs/outputs, not just its label — the label can be wrong or absent.

2. **For each wrap TX**, compute the wrap fee directly: `sats locked - frBTC minted = sats withheld`. Express it as a percentage of the locked amount. This is a real, observable fee even if nothing calls it that.

3. **For each unwrap TX**, note the frBTC burned and flag that the payout has *not yet happened* — it lives in a future dispatch TX, not this one. Don't count BTC "returned" in the unwrap TX as the payout; check whether it's actually the user's own carrier UTXO being recycled (common) versus a genuine protocol release (rare, only for the original reserve).

4. **Find the matching dispatch TX** for each unwrap (search subsequent wdsx7-address transactions for an output matching the user's address, within the observed lag window). Compute:
   - **Expected payout** — either the original locked reserve (for the first unwrap in a chain) or a proportional release: `original_reserve × (frBTC_burned_this_unwrap / frBTC_originally_minted)`.
   - **Actual payout** — the literal output amount to the user in the dispatch TX.
   - **Shortfall** — expected minus actual, in sats and as a percentage. A consistent shortfall across multiple independent dispatches (not just rounding noise on one) is the strongest evidence of an undisclosed fee — especially if it contradicts an explicit "no protocol fees" claim from the team. State the contradiction plainly if the data shows one; don't soften it into "may be a fee."

5. **Build a cost breakdown** attributing the total BTC lost (start balance minus end balance, ignoring what's still parked in open positions) across categories: miner fees (sum every TX's fee), AMM slippage (round-trip swap losses), protocol dust (flat per-TX dust outputs to the protocol address — note these often partially return to the user too), and dispatch residual/shortfall (the unexplained gap from step 4). Assign each a `%` of total loss and mark whether it's expected/disclosed or not.

6. **State the net result** as start balance → end balance → net change, then hand back the cost breakdown as the explanation, ordered by size, largest driver first (miner fees are typically the majority of loss, not the protocol fee itself — say so if that's what the data shows, don't lead with the most suspicious-sounding number just because it's more interesting).

## Output shape

- Per-TX table: TX #, TXID, classification, BTC/frBTC in, BTC/frBTC out, net, one-line note.
- Wrap fee table: locked sats → minted frBTC → withheld sats → %.
- Dispatch reconciliation table: unwrap TX → expected payout → actual payout → shortfall (sats, %) → verdict (expected/unexplained).
- Cost breakdown table: category → sats → % of total loss → expected or not.
- One paragraph net summary, leading with the largest cost driver.
