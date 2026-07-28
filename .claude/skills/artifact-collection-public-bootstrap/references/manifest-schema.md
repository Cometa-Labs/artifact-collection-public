# manifest.json schema

`documents/manifest.json` in `artifact-collection-public` is a JSON array of `Artifact` objects. It must stay byte-for-byte compatible with the `Artifact` type consumed by the `artifact-collection` app (`lib/artifacts.ts`) — that app does zero runtime validation on the fetched JSON, so a malformed or mistyped field doesn't throw, it just silently renders wrong (or breaks the route for that slug).

## Type

```ts
type Artifact = {
  slug: string;
  title: string;
  eyebrow: string;
  summary: string;
  file: string;
  date: string;
  type: "Report" | "Model" | "Calculator" | "Map" | "Product";
  indexCode: string;
  status: "Reference" | "Active" | "Exploratory";
  agentUse: string;
  tags: string[];
};
```

## Field-by-field

| Field | Rules | Used for |
|---|---|---|
| `slug` | kebab-case, `^[a-z0-9]+(-[a-z0-9]+)*$`, globally unique | Route: `artifact-collection.app/artifacts/<slug>`. Never reuse or change an existing slug — it's a public URL. |
| `title` | Short human title | Card heading, `<h1>` on detail page, page `<title>` |
| `eyebrow` | Short category label (2-3 words), e.g. "Market structure", "Product Research" | Small label above title on card and detail page |
| `summary` | 1-2 sentences | Card body, meta description, OpenGraph/Twitter description |
| `file` | Bare filename only (no path), must exist as a sibling file in `documents/` in this repo, e.g. `"5layersVC.html"` | Joined with the CDN base URL: `.../documents/<file>` |
| `date` | `YYYY-MM-DD` | Parsed as `new Date(\`${date}T00:00:00\`)` and formatted for display; also sortable via string comparison, so the format must stay zero-padded and ISO-ordered |
| `type` | One of exactly: `"Report"`, `"Model"`, `"Calculator"`, `"Map"`, `"Product"` (case-sensitive) | Badge, sort-by-type, filter |
| `indexCode` | `<PREFIX>-<3-digit-number>`, globally unique, e.g. `"OPS-001"`, `"AI-002"` | Badge, search index, SEO keywords |
| `status` | One of exactly: `"Reference"`, `"Active"`, `"Exploratory"` (case-sensitive) | Badge, card metadata |
| `agentUse` | 1 sentence, imperative, written for an LLM reading the catalog (e.g. "Use to reason about VC workflow layers, handoffs, and operating leverage.") | Detail page metadata, `x-agent-use` meta tag |
| `tags` | Array of short strings, Title Case, 2-5 per item | Filter chips, search index |

## `indexCode` numbering convention

The numeric suffix increments **globally across the whole manifest**, not per prefix — it is not reset per category. To pick the next one: find the highest `NNN` currently in use across every entry, and use `highest + 1`, regardless of which prefix that highest entry has.

Existing prefixes in use (not exhaustive — pick a new one if the item doesn't fit):

| Prefix | Category |
|---|---|
| `OPS` | Operations / execution models |
| `AI` | AI platforms, tokens, models |
| `MKT` | Market structure, competitor/landscape maps |
| `BTCFI` | Bitcoin/DeFi-specific research |
| `FUND` | Fund/investor product research |
| `GACHA` | Game design / monetization mechanics |

## Example entry

```json
{
  "slug": "btc-flow-analysis",
  "title": "BTC Flow Analysis",
  "eyebrow": "Market structure",
  "summary": "Flow-oriented Bitcoin analysis covering supply movement and market signal framing.",
  "file": "btc_flow_analysis.html",
  "date": "2026-07-21",
  "type": "Report",
  "indexCode": "MKT-003",
  "status": "Reference",
  "agentUse": "Use for Bitcoin supply-flow framing, market signal interpretation, and memo context.",
  "tags": ["Bitcoin", "Markets", "Flow"]
}
```

See `assets/example-manifest.json` for a complete, valid manifest with multiple entries, and `scripts/validate_manifest.py` to check a manifest against these rules programmatically.
