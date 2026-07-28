# artifact-collection-public repo layout

```
artifact-collection-public/
├── README.md
├── LICENSE                                    All Rights Reserved — see assets/LICENSE.template
├── documents/
│   ├── manifest.json                          One JSON array, see references/manifest-schema.md
│   ├── btc_flow_analysis.html
│   ├── btcfi_history_hype_vs_real_2.html
│   └── ...                                    One self-contained .html per manifest entry
└── skills/
    ├── manifest.json                          One JSON array, see references/skills-schema.md
    └── <slug>/
        └── SKILL.md                           Real skill folder, not just a metadata row — see references/skills-schema.md
```

## Why this exact shape

The consuming app (`artifact-collection`) shares one CDN base (`lib/cdn.ts`) across both `documents/` and `skills/`:

```ts
const DOCS_REPO = "Cometa-Labs/artifact-collection-public";
const DOCS_BRANCH = "main";
const CDN_BASE = `https://cdn.jsdelivr.net/gh/${DOCS_REPO}@${DOCS_BRANCH}`;
// lib/artifacts.ts: `${CDN_BASE}/documents/manifest.json`
// lib/skills.ts:    `${CDN_BASE}/skills/manifest.json`
```

- The repo must be named `artifact-collection-public` under the `Cometa-Labs` org, on the `main` branch — any of these changing requires updating the constants in the consuming app's `lib/cdn.ts` too.
- The folders **must** be named `documents/` and `skills/` at the repo root — those are the fixed path segments in `CDN_BASE`.
- Each `manifest.json` **must** live directly inside its own folder, not at the repo root.
- Every `file` referenced from a `documents/manifest.json` entry must be a sibling of that manifest inside `documents/` — no subfolders.
- Every `slug` referenced from a `skills/manifest.json` entry must have a matching `skills/<slug>/` folder containing at least a `SKILL.md` — the app's file explorer reads that folder's tree directly via jsDelivr's package-metadata API.
- The repo must be **public** — jsDelivr's `gh/` endpoint only serves public GitHub repos, no auth token is ever passed.

## Initializing from scratch

```bash
mkdir artifact-collection-public && cd artifact-collection-public
git init
mkdir documents skills
echo "[]" > documents/manifest.json   # or seed with assets/example-manifest.json + assets/documents/*.html (BTC docs only, see SKILL.md step A)
echo "[]" > skills/manifest.json      # or seed with assets/skills-manifest.json + assets/skills/*/SKILL.md (one worked example, see SKILL.md step A)
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

For a skill, purge `skills/manifest.json` plus every file under the new `skills/<slug>/` folder the same way:

```bash
curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/skills/manifest.json"
curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/skills/<slug>/SKILL.md"
```

Note: the app's file explorer for a skill's folder reads the tree from jsDelivr's separate package-metadata API (`data.jsdelivr.com`), not from the CDN file endpoint above — that API has its own cache with no officially documented purge endpoint, so a brand-new skill's file listing may lag behind the manifest/file purge by longer than usual. Without any manual purge, everything still converges on its own: the consuming app re-fetches within an hour (`next: { revalidate: 3600 }` across `lib/artifacts.ts` / `lib/skills.ts` / `lib/cdn.ts`), and jsDelivr's caches expire on their own schedule regardless.
