# skills/ layout and manifest.json schema

Skills are real folders, not metadata rows. `skills/manifest.json` is the index; each entry's actual content lives in its own `skills/<slug>/SKILL.md` (optionally plus `references/`, `scripts/`, `assets/` — same conventions as any Claude Code skill, see the `skill-creator` skill if those subfolders are needed).

```
documents/
  manifest.json
  *.html
skills/
  manifest.json                    One JSON array, schema below
  <slug>/
    SKILL.md                       Frontmatter (name, description) + the generalized playbook body
    references/                    Optional
    scripts/                       Optional
    assets/                        Optional
```

## Type

```ts
type Skill = {
  slug: string;
  name: string;
  indexCode: string;
  category: "Research" | "Operations" | "Market" | "Product" | "AI";
  summary: string;
  whenToUse: string;
  inputs: string[];
  outputs: string[];
  relatedArtifacts: string[];
  tags: string[];
};
```

## Field-by-field

| Field | Rules | Used for |
|---|---|---|
| `slug` | kebab-case, `^[a-z0-9]+(-[a-z0-9]+)*$`, globally unique, must match the folder name `skills/<slug>/` | Route: `artifact-collection.app/skills/<slug>`, and the folder the app's file explorer reads |
| `name` | Short human title | Card heading, `<h1>` on the skill page |
| `indexCode` | `SKILL-<3-digit-number>`, globally unique, sequential (find the highest existing number across the manifest, use `+1`) | Badge, search index |
| `category` | One of exactly: `"Research"`, `"Operations"`, `"Market"`, `"Product"`, `"AI"` (case-sensitive) | Filter, badge |
| `summary` | 1-2 sentences | Card body |
| `whenToUse` | 1 sentence, the trigger condition | Card metadata, skill page |
| `inputs` | Array of short strings | Card metadata |
| `outputs` | Array of short strings | Card metadata |
| `relatedArtifacts` | Array of `slug`s from `documents/manifest.json` | Cross-links on the card and skill page; entries that don't match a known artifact slug are still rendered (as plain text) rather than erroring |
| `tags` | Array of short strings, Title Case | Filter chips |

## `SKILL.md` requirements

- Real YAML frontmatter: `name` (matches the manifest `slug`) and `description` (states what it does and when to trigger it — see the skill-writing guidance in `skill-creator` for tone).
- The body must open, immediately after the frontmatter, with this caveat (verbatim or close to it) — every extracted skill carries it, no exceptions:
  > Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.
- The rest of the body is the generalized procedure — see `assets/skills/frbtc-flow-tracing/SKILL.md` for a full worked example of the expected depth and structure.

## Example manifest entry

```json
{
  "slug": "frbtc-flow-tracing",
  "name": "frBTC Wrap/Unwrap Flow Tracing",
  "indexCode": "SKILL-001",
  "category": "Research",
  "summary": "Trace a chain of frBTC wrap/swap/unwrap/dispatch transactions to compute net BTC flow, expected vs actual payouts, and flag undisclosed fees.",
  "whenToUse": "Use when auditing a Bitcoin address's wdsx7/frBTC/Alkanes transaction history to verify wrap fees, deferred dispatch payouts, and whether stated 'no fee' claims hold up against on-chain data.",
  "inputs": ["Address's transaction list (TXIDs, confirmations)", "Per-TX inputs/outputs with BTC and frBTC amounts", "Any protocol fee claims to verify"],
  "outputs": ["Per-TX flow breakdown (wrap/swap/unwrap/dispatch classification)", "Expected vs actual payout deltas", "Cost breakdown by category", "Net BTC flow summary"],
  "relatedArtifacts": ["btc-flow-analysis"],
  "tags": ["Bitcoin", "BTCFi", "Flow Analysis", "Audit"]
}
```

See `assets/skills-manifest.json` + `assets/skills/frbtc-flow-tracing/` for the full worked seed example, and `scripts/validate_skills_manifest.py` to check a manifest against these rules programmatically. Skill extraction itself (discovery → interview → write) is a separate skill — see `assets/skill-extraction/`.
