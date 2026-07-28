# artifact-collection-public

Public document store for the [Cometa Labs Knowledgebase](https://artifact-collection.vercel.app). This repo holds the self-contained HTML artifacts and their metadata manifest, served to the app via [jsDelivr's GitHub CDN](https://www.jsdelivr.com/?docs=gh) — no build step, no server, no auth.

This repo is public so the app can read it, not so its contents can be reused. See [License](#license) below — public readability is not a license grant.

The consuming app fetches `documents/manifest.json` at request time (revalidated hourly) and renders each artifact's `documents/<file>.html` directly in an iframe. Pushing here updates the live knowledgebase without a redeploy of the app itself.

## Structure

```
documents/
  manifest.json   Metadata for every artifact — see schema below
  *.html          One self-contained HTML file per manifest entry
```

## Adding a document

1. Author or drop in a self-contained `.html` file — no external `<script src>`/`<link href>`, no calls to a live backend. Run the `html-artifact-audit` skill (`.claude/skills/html-artifact-audit`, installed in this repo), or manually check:
   - Every `target="_blank"` link has `rel="noopener noreferrer"`.
   - No `<script src="http...">` or `<link href="http...">`.
   - No `fetch()`/XHR call with a literal URL argument.
2. Add it to `documents/`.
3. Add a matching entry to `documents/manifest.json` (schema below).
4. Commit and push to `main`.
5. Optional — force an immediate CDN refresh instead of waiting for jsDelivr's cache to expire:
   ```bash
   curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/manifest.json"
   curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/<file>.html"
   ```

## `manifest.json` schema

```ts
type Artifact = {
  slug: string;        // kebab-case, unique, becomes the app route /artifacts/<slug>
  title: string;
  eyebrow: string;      // short category label
  summary: string;      // 1-2 sentences
  file: string;         // bare filename in this documents/ folder
  date: string;         // YYYY-MM-DD
  type: "Report" | "Model" | "Calculator" | "Map" | "Product";
  indexCode: string;    // "<PREFIX>-<3-digit-number>", globally unique, sequential
  status: "Reference" | "Active" | "Exploratory";
  agentUse: string;     // one sentence written for an LLM reading the catalog
  tags: string[];
};
```

## License

All Rights Reserved — Copyright (c) 2026 Cometa Labs. This repo is made publicly readable solely so the Cometa Labs Knowledgebase app (and any party Cometa Labs authorizes) can display its contents. That does not grant any license to use, copy, modify, or redistribute the contents. See [`LICENSE`](./LICENSE) for the full terms.
