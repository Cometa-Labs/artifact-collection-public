---
name: btcfi-hype-vs-real-rubric
description: Classify a BTCfi (Bitcoin-DeFi) claim, protocol, or narrative as Real, Hype, or Mixed/jury's-out using a checklist derived from BTCfi's actual history (wBTC, Ordinals, BRC-20, Runes, Babylon, BitVM). Use when asked whether a new Bitcoin-DeFi project, yield narrative, or "trustless" bridge claim is substantive infrastructure or speculative froth.
---

# BTCfi hype-vs-real rubric

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes the scorecard method used to evaluate BTCfi's history (wBTC, Taproot, Ordinals, BRC-20, Runes, Alkanes, the wBTC custody crisis, Babylon, BitVM) into a repeatable checklist for judging a *new* BTCfi claim, protocol, or narrative the same way.

## The core pattern from BTCfi's history

Looking back across BTCfi eras, "real" and "hype" consistently separated along the same lines:

- **Real** turned out to mean: a mechanism that doesn't require trusting a new custodian (Babylon's self-custodial staking, Taproot's cryptography, Ordinals' proof that Bitcoin can durably store data), or infrastructure that later projects build on regardless of whether the original hype cycle survived (Ordinals' data layer outlived the NFT mania; Taproot's Schnorr sigs underpin everything after it).
- **Hype** turned out to mean: valuations or "yield" detached from an underlying mechanism (BRC-20 meme token market caps, point-farming APYs promising future airdrops), or a solution whose core assumption is "just trust this custodian/committee" dressed up as decentralized (wBTC, cbBTC, BTCB).
- **Mixed / jury's out** turned out to mean: the mechanism is technically real but has an unresolved trust or scaling assumption that hasn't been tested under adversarial conditions yet (Alkanes' indexer-as-consensus risk, BitVM's computational cost, Babylon Phase-1's "staking with no yield yet").

## Procedure

1. **Identify the mechanism**, separate from the narrative. What does the protocol actually do on-chain (or claim to do)? Write this down before reading any marketing framing — e.g. "locks BTC in a timelock script, no bridge" vs. "revolutionary BTC staking."

2. **Run the trust-and-custody check.** Does using this require trusting a centralized custodian or a permissioned committee with your BTC? If yes, it inherits the wBTC-style trust trade-off no matter what it's branded as — flag it as at least partially hype, regardless of TVL or excitement.

3. **Run the valuation-vs-mechanism check.** Is the number everyone's excited about (market cap, APY, TVL) backed by real usage/revenue, or by speculative trading and a future token promise? Point-farming and pre-airdrop "yield" default to hype until the promised token lands and real economics are observed.

4. **Run the adversarial/scale test.** Has the mechanism been tested at scale, under real adversarial conditions (large capital, contested state, indexer disagreement)? If the theory is sound but this hasn't happened yet, that's "jury's out," not "real" — don't upgrade something to real just because the cryptography is elegant.

5. **Check for indexer/consensus fragility.** If correctness depends on off-chain indexers agreeing with each other (as BRC-20 and Alkanes-style metaprotocols do), note that a disagreement among major indexers is a real, demonstrated failure mode (BRC-20's 2024 split), not a hypothetical risk.

6. **Classify:** Real / Hype / Mixed, and write one sentence each for what's real and what's hype about it — don't collapse a mixed case into a single verdict. Most claims worth evaluating are mixed; a clean "real" or "hype" is the exception, not the default.

## Output shape

- One-line mechanism description (not the marketing pitch).
- Four checks above, each with a short answer.
- Verdict: Real / Hype / Mixed, with a "what's real" and "what's hype" line for mixed cases (mirroring the source document's verdict-card format).
