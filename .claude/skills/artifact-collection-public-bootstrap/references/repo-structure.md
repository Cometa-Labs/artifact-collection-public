# artifact-collection-public repo layout

```
artifact-collection-public/
├── README.md
├── LICENSE                                    All Rights Reserved — see assets/LICENSE.template
└── documents/
    ├── manifest.json                          One JSON array, see references/manifest-schema.md
    ├── btc_flow_analysis.html
    ├── btcfi_history_hype_vs_real_2.html
    └── ...                                    One self-contained .html per manifest entry
```

## Why this exact shape

The consuming app (`artifact-collection`, `lib/artifacts.ts`) hardcodes:

```ts
const DOCS_REPO = "Cometa-Labs/artifact-collection-public";
const DOCS_BRANCH = "main";
const DOCS_CDN_BASE = `https://cdn.jsdelivr.net/gh/${DOCS_REPO}@${DOCS_BRANCH}/documents`;
const MANIFEST_URL = `${DOCS_CDN_BASE}/manifest.json`;
```

- The repo must be named `artifact-collection-public` under the `Cometa-Labs` org, on the `main` branch — any of these changing requires updating the constants in the consuming app's `lib/artifacts.ts` too.
- The folder **must** be named `documents/` at the repo root — that's the fixed path segment in `DOCS_CDN_BASE`.
- `manifest.json` **must** live directly inside `documents/`, not at the repo root.
- Every `file` referenced from a manifest entry must be a sibling of `manifest.json` inside `documents/` — no subfolders, since the app builds URLs as `${DOCS_CDN_BASE}/${artifact.file}` with no path prefix.
- The repo must be **public** — jsDelivr's `gh/` endpoint only serves public GitHub repos, no auth token is ever passed.

## Initializing from scratch

```bash
mkdir artifact-collection-public && cd artifact-collection-public
git init
mkdir documents
echo "[]" > documents/manifest.json   # or seed with assets/example-manifest.json + assets/documents/*.html (BTC docs only, see SKILL.md step A)
```

Then add a README (see `assets/README.md.template`) and a `LICENSE` (see `assets/LICENSE.template` — All Rights Reserved, not open source), commit, and push to `main` on the `Cometa-Labs` org under the exact name `artifact-collection-public`.

## Publishing changes

After adding/updating a `.html` file and its `manifest.json` entry:

```bash
git add documents/
git commit -m "Add <artifact title>"
git push origin main
```

jsDelivr caches the `@main` ref for up to ~12-24h. To force an immediate refresh after pushing:

```bash
curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/manifest.json"
curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/<file>.html"
```

Without a manual purge, the consuming app still picks up the change on its own within an hour (`next: { revalidate: 3600 }` in `lib/artifacts.ts`), and jsDelivr's own cache will eventually expire too — the purge just makes both immediate.
