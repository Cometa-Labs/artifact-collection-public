---
name: artifact-collection-public-bootstrap
description: Bootstrap and maintain the artifact-collection-public GitHub repo — the public, jsDelivr-CDN-served document and skill store that powers the Cometa Labs Knowledgebase app (artifact-collection). Covers initializing the repo from scratch (documents/ folder, skills/ folder, manifests, README, LICENSE), auditing and writing new self-contained HTML artifacts, summarizing an artifact into a manifest.json entry per the Artifact schema, validating manifests, publishing (commit, push, jsDelivr cache purge), removing an item, and reminding the user to run skill extraction on newly published documents. Use this whenever the user wants to create/initialize the "artifact-collection-public" repo, add a new knowledge item / artifact / report / calculator / map to the shared knowledgebase, edit or generate documents/manifest.json or skills/manifest.json, publish an HTML document to the CDN-backed docs store, remove/delete/take down/unpublish a document from it, or extract/generate a skill from a document — even if they don't reference this skill or repo by name. Always surface the publishing-clearance and removal-limitation warnings in references/publishing-and-removal.md when either adding or removing content — do not skip them because the user seems confident.
---

# artifact-collection-public bootstrap

`artifact-collection-public` is a public GitHub repo that exists purely to be read by the `artifact-collection` Next.js app over jsDelivr's GitHub CDN — no server, no build step, no auth. Pushing to `main` here updates the live knowledgebase without redeploying the app. This skill covers the full lifecycle: initializing the repo, adding artifacts, keeping manifests valid, publishing, removing an item, and prompting for skill extraction.

Read `references/repo-structure.md` before doing anything structural (init, moving folders, changing the repo/branch name) — the consuming app hardcodes the exact repo name, branch, and folder path, and any drift breaks the fetch.

## A. Initialize the repo (first time only)

1. Create the repo `Cometa-Labs/artifact-collection-public`, public visibility.
2. Build the layout from `references/repo-structure.md`:
   ```
   artifact-collection-public/
   ├── README.md
   ├── LICENSE
   ├── documents/
   │   ├── manifest.json
   │   ├── btc_flow_analysis.html
   │   └── btcfi_history_hype_vs_real_2.html
   └── skills/
       ├── manifest.json
       └── frbtc-flow-tracing/
           └── SKILL.md
   ```
3. Write `README.md` from `assets/README.md.template` (fill in nothing — it's already generic and correct for this repo).
4. Write `LICENSE` from `assets/LICENSE.template` (All Rights Reserved — this repo is public for CDN readability only, not open source; do not substitute a permissive license like MIT).
5. Seed `documents/manifest.json` and `documents/` with the two BTC artifacts only:
   ```bash
   cp <this-skill-dir>/assets/example-manifest.json artifact-collection-public/documents/manifest.json
   cp <this-skill-dir>/assets/documents/*.html artifact-collection-public/documents/
   ```
   This bundle intentionally contains only `btc-flow-analysis` and `btcfi-history-hype-vs-real` — a small, real, working example, not the full catalog. **Do not** bulk-copy the rest of the `artifact-collection` app's `public/documents/` into the new repo as part of init. Any other existing artifact must be migrated one at a time through the normal **B. Add a new knowledge item** flow below (audit → summarize → validate) so each one gets the same scrutiny a brand-new artifact would.
6. Seed `skills/manifest.json` and `skills/` with one worked example skill, extracted from `btc-flow-analysis`:
   ```bash
   cp <this-skill-dir>/assets/skills-manifest.json artifact-collection-public/skills/manifest.json
   cp -r <this-skill-dir>/assets/skills/frbtc-flow-tracing artifact-collection-public/skills/frbtc-flow-tracing
   ```
   Same rule as documents: this is one real, worked example (`frbtc-flow-tracing`), not a bulk migration of any pre-existing skill catalog. Any other skill must go through the **skill-extraction** flow (see step 7 and the reminder at the end of Section C) so it gets the same discovery/interview scrutiny.
7. **Install `html-artifact-audit` and `skill-extraction` into the new repo** so both are available to Claude Code whenever someone works in `artifact-collection-public` directly, not just via this bootstrap package:
   ```bash
   mkdir -p artifact-collection-public/.claude/skills
   cp -r <this-skill-dir>/assets/html-artifact-audit artifact-collection-public/.claude/skills/html-artifact-audit
   cp -r <this-skill-dir>/assets/skill-extraction artifact-collection-public/.claude/skills/skill-extraction
   cp <this-skill-dir>/assets/settings.json.template artifact-collection-public/.claude/settings.json
   ```
   If `artifact-collection-public/.claude/settings.json` already exists (e.g. re-running init), merge `".claude/skills/html-artifact-audit"` and `".claude/skills/skill-extraction"` into its `"skills"` array instead of overwriting the file.
8. `git init`, commit (including `.claude/`), push to `main`.
9. Validate before the first push: `python3 scripts/validate_manifest.py documents` and `python3 scripts/validate_skills_manifest.py skills`.

## B. Add a new knowledge item

1. **Confirm publishing clearance first, before anything else.** Ask the user to confirm the document has been cleared by legal or a team lead to be made public — don't assume it has been just because they asked you to add it. This repo is public and effectively impossible to fully walk back once something is pushed (see `references/publishing-and-removal.md`). If clearance hasn't been confirmed, stop here and ask; do not proceed to audit or write the manifest entry.

2. **Get or write the HTML file.** It must be fully self-contained — read `references/html-artifact-format.md` for what that means and why (jsDelivr serves the raw file with nothing else resolving relative to it). Use `assets/example-artifact.html` as a starting skeleton for a new file.

3. **Audit it** — run:
   ```bash
   ./scripts/audit_html.sh documents/<new-file>.html
   ```
   - Any `FAIL` (missing `rel="noopener noreferrer"` on a `target="_blank"` link) must be fixed before proceeding — it's a reverse-tabnabbing bug, not a style nit.
   - Any `REVIEW` (external script/link src, or a `fetch()`/XHR call with a literal URL) needs your judgment, not an automatic fix. Check `references/html-artifact-format.md`'s note on minified libraries — a `fetch(` match inside a bundled dependency that never resolves to a literal URL is a false positive and fine to ignore; a real call to a live endpoint is not and means the artifact isn't actually self-contained.

4. **Summarize it into a manifest entry.** Read enough of the file to fill every field faithfully — don't invent claims the document doesn't support. Follow `references/manifest-schema.md` exactly, in particular:
   - `slug`: kebab-case, unique, becomes a permanent public URL — get it right the first time.
   - `indexCode`: find the highest `NNN` currently used anywhere in the manifest (across all prefixes) and use `+1`. Pick an existing prefix from the table in `references/manifest-schema.md` if the topic fits, otherwise a new short all-caps prefix.
   - `agentUse`: written for an LLM reading the catalog later, not for a human — one imperative sentence about when to reach for this artifact.
   - `type`/`status`: must be exactly one of the literal values listed in the schema — these are case-sensitive and unvalidated at runtime by the consuming app, so a typo here silently breaks filtering instead of erroring.

5. **Append the entry** to `documents/manifest.json` and **validate**:
   ```bash
   python3 scripts/validate_manifest.py documents
   ```
   Fix everything it reports before moving on — it checks slug/indexCode format and uniqueness, enum values, date format, and that `file` actually exists in `documents/`.

## C. Publish

```bash
git add documents/
git commit -m "Add <artifact title>"
git push origin main
```

Optional — force an immediate CDN refresh (otherwise jsDelivr's cache expires on its own within ~12-24h, and the consuming app re-fetches within an hour regardless):

```bash
curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/manifest.json"
curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/<file>.html"
```

Confirm the item shows up at `https://cdn.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/manifest.json` before considering it done.

**Now that the document is live, remind the user to consider skill extraction.** Ask: does this document contain a repeatable procedure worth capturing as a reusable skill, or is it just a finding/report? If it's plausibly the former, point them at the `skill-extraction` skill (installed at `.claude/skills/skill-extraction` in this repo per step A.7) to run its discovery → interview flow against the document just published. This is a prompt, not an automatic action — don't run skill-extraction yourself as part of this publish step; it's a separate, deliberately interactive process that needs the user's input at the interview stage.

## D. Remove a knowledge item

> **Before doing this, tell the user plainly: removing an item stops the app from listing/serving it going forward, but does not erase the fact that it was public.** Once something is pushed to `main` on this repo, treat it as permanently, irrevocably available somewhere — git history, existing forks/clones, commit-pinned jsDelivr URLs, and search/archive crawlers can all keep serving or exposing it independent of anything done here. Read `references/publishing-and-removal.md` in full before removing anything, and surface its warning to the user rather than silently deleting and moving on. If the reason for removal is that something sensitive was published, say so explicitly and treat it as a disclosure matter for the user/legal to weigh in on, not just a file deletion.

1. Remove the entry from `documents/manifest.json`.
2. Delete the corresponding `.html` file from `documents/`.
3. Validate the manifest is still well-formed: `python3 scripts/validate_manifest.py documents`.
4. Commit with a clear message (e.g. `Remove <artifact title>`) and push to `main`.
5. Purge the jsDelivr cache for both the manifest and the removed file, same as a normal publish:
   ```bash
   curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/manifest.json"
   curl "https://purge.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/<file>.html"
   ```
6. Tell the user the item is delisted from the live knowledgebase, and remind them (again, briefly) that this doesn't retroactively un-expose it — see the bottom-line note in `references/publishing-and-removal.md` if there's any real sensitivity involved (git history rewrite is a separate, deliberate decision, not a default step here).

## Bundled resources

- `references/repo-structure.md` — exact repo layout (`documents/` and `skills/`) and why each part of it is fixed by the consuming app
- `references/manifest-schema.md` — full `Artifact` field reference, `indexCode` convention, worked example
- `references/html-artifact-format.md` — what "self-contained HTML" means here, minimal skeleton, note on interactive/bundled artifacts
- `references/skills-schema.md` — `skills/` folder layout, `Skill` manifest field reference, `SKILL.md` requirements (including the mandatory auto-generated caveat)
- `references/publishing-and-removal.md` — the pre-publish legal/team-lead clearance gate, and what removing an item does and doesn't actually undo
- `scripts/audit_html.sh` — pre-flight audit for a new HTML file (reverse-tabnabbing, external deps, live-backend calls)
- `scripts/validate_manifest.py` — validates `documents/manifest.json` against the schema
- `scripts/validate_skills_manifest.py` — validates `skills/manifest.json` against the schema, including that each entry's `SKILL.md` actually exists
- `assets/example-artifact.html` — starting skeleton for a new artifact
- `assets/example-manifest.json` — a small, real, valid manifest (the two BTC artifacts only) — reference for the schema and seed data for init, deliberately not the full catalog (see step A.5)
- `assets/documents/*.html` — the real HTML files backing `example-manifest.json` (`btc_flow_analysis.html`, `btcfi_history_hype_vs_real_2.html`), already audited and fixed
- `assets/skills-manifest.json` + `assets/skills/frbtc-flow-tracing/SKILL.md` — one real, worked example skill extracted from `btc-flow-analysis`, used as init seed data (see step A.6) and as the depth/structure reference for anything `skill-extraction` writes
- `assets/README.md.template` — drop-in `README.md` for the new repo
- `assets/LICENSE.template` — drop-in `LICENSE` for the new repo (All Rights Reserved, not open source)
- `assets/html-artifact-audit/` — a full copy of the `html-artifact-audit` skill, installed into the new repo during init (step A.7) so Claude Code has it available there directly
- `assets/skill-extraction/` — a full copy of the `skill-extraction` skill (discovery → interview → write a real `skills/<slug>/SKILL.md`), installed into the new repo during init (step A.7)
- `assets/settings.json.template` — `.claude/settings.json` for the new repo, registering `html-artifact-audit` and `skill-extraction`
