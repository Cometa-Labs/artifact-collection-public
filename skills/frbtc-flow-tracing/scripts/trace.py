#!/usr/bin/env python3
"""
frBTC wrap/unwrap flow tracer.

Fetches an address's transaction history from a Bitcoin explorer (Esplora-style
REST API, e.g. mempool.space or Blockstream) for raw BTC amounts, and from an
Alkanes/Metashrew indexer for protocol-level state (frBTC mint/burn amounts,
wdsx7 reserve balances) that a plain Bitcoin explorer cannot see.

Two data sources are required because this is a metaprotocol: Bitcoin's own
UTXO set has no concept of frBTC or a "wdsx7 reserve" — that state only exists
in Alkanes contract storage, which is computed by replaying witness-envelope
WASM execution against Bitcoin chaindata and served by a Metashrew-compatible
indexer (e.g. a subfrost/Alkanes RPC endpoint). Adjust ALKANES_INDEXER_URL to
whatever indexer endpoint you have access to; the request/response shape below
is illustrative and will need to match your indexer's actual API.

Usage:
    python trace.py <address> [--explorer https://mempool.space/api] [--alkanes-indexer https://your-indexer/rpc]
"""
import argparse
import json
import sys
import urllib.request


def fetch_json(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def fetch_address_txs(explorer_base, address):
    """Esplora-style: GET /address/:address/txs"""
    return fetch_json(f"{explorer_base}/address/{address}/txs")


def fetch_tx(explorer_base, txid):
    """Esplora-style: GET /tx/:txid"""
    return fetch_json(f"{explorer_base}/tx/{txid}")


def fetch_alkanes_state(indexer_base, txid):
    """
    Placeholder call to an Alkanes/Metashrew indexer for protocol-level
    annotations on a tx: frBTC minted/burned amounts, which outputs are
    wdsx7 reserve locks, and dispatch-batch linkage back to the unwrap TX
    that triggered it. Replace with your indexer's real method name/schema.
    """
    return fetch_json(
        f"{indexer_base}",
        method="POST",
        payload={"method": "alkanes_getTxAnnotations", "params": [txid]},
    )


def classify_tx(btc_tx, alkanes_annotations):
    """
    Classify a tx as wrap / swap / unwrap / dispatch by inspecting inputs and
    outputs rather than trusting any label — see SKILL.md step 1. This stub
    only sketches the shape; fill in real opcode/address checks for your
    protocol version.
    """
    if alkanes_annotations.get("frbtc_minted"):
        return "wrap"
    if alkanes_annotations.get("frbtc_burned") and not alkanes_annotations.get("wdsx7_is_input"):
        return "unwrap"
    if alkanes_annotations.get("wdsx7_is_input"):
        return "dispatch"
    if alkanes_annotations.get("frbtc_swapped"):
        return "swap"
    return "unknown"


def reconcile(address, explorer_base, indexer_base):
    txs = fetch_address_txs(explorer_base, address)
    rows = []
    for tx_summary in txs:
        txid = tx_summary["txid"]
        tx = fetch_tx(explorer_base, txid)
        annotations = fetch_alkanes_state(indexer_base, txid)
        kind = classify_tx(tx, annotations)
        rows.append({
            "txid": txid,
            "kind": kind,
            "fee_sats": tx.get("fee"),
            "frbtc_minted": annotations.get("frbtc_minted"),
            "frbtc_burned": annotations.get("frbtc_burned"),
            "wdsx7_locked_sats": annotations.get("wdsx7_locked_sats"),
        })

    # Wrap fee: sats locked - frBTC minted, per SKILL.md step 2.
    for r in rows:
        if r["kind"] == "wrap" and r["wdsx7_locked_sats"] and r["frbtc_minted"]:
            withheld = r["wdsx7_locked_sats"] - r["frbtc_minted"]
            r["wrap_fee_sats"] = withheld
            r["wrap_fee_pct"] = withheld / r["wdsx7_locked_sats"] * 100

    # Dispatch shortfall: match each unwrap to its later dispatch tx and
    # compare expected (proportional reserve release) vs actual payout,
    # per SKILL.md step 4. Matching logic is protocol/indexer-specific —
    # left as an exercise since it depends on how your indexer links them.

    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("address")
    ap.add_argument("--explorer", default="https://mempool.space/api",
                     help="Esplora-style Bitcoin explorer API base URL")
    ap.add_argument("--alkanes-indexer", required=True,
                     help="Alkanes/Metashrew indexer RPC base URL for frBTC/wdsx7 state")
    args = ap.parse_args()

    rows = reconcile(args.address, args.explorer, args.alkanes_indexer)
    json.dump(rows, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
