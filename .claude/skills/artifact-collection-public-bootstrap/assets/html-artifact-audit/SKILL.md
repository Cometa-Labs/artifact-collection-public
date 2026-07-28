---
name: html-artifact-audit
description: Audit a self-contained HTML artifact before it is added to the knowledgebase (public/documents or the public artifact-collection-public repo). Use whenever ingesting, generating, or updating an .html document for this project — checks for reverse-tabnabbing links, inline/external script risk, and embedded fetch/XHR calls to unexpected origins.
---

# HTML Artifact Audit

Knowledgebase artifacts are trusted, self-contained `.html` files rendered directly in an iframe on the same origin as the app (or, once the CDN migration lands, fetched from a public GitHub-backed CDN). Before adding or updating one, run this audit — it's cheap and catches the two failure modes that actually matter here.

## 1. `target="_blank"` without `rel="noopener noreferrer"`

Any anchor that opens in a new tab must also isolate that tab from the origin document (reverse tabnabbing — the opened page could otherwise navigate the original tab via `window.opener`).

Check:

```bash
grep -oE '<a [^>]*target="_blank"[^>]*>' <file>.html | grep -v 'rel="noopener'
```

Any line printed is missing the attribute. Fix by adding `rel="noopener noreferrer"` to the tag.

## 2. Unexpected external script/style dependencies

Artifacts should be fully self-contained — no external `<script src>` or `<link href>` pointing off-origin. This matters for the CDN migration in particular: `cdn.jsdelivr.net` will serve the file byte-for-byte, so any relative asset path or same-origin API assumption baked into the file will silently break.

Check:

```bash
grep -oE '<(script|link)[^>]*(src|href)="[^"]*"' <file>.html
```

Anything pointing to `http(s)://` (other than plain citation `<a href>` links a human clicks) or to a relative path outside the file itself is a red flag — flag it to the user rather than silently shipping it.

## 3. Embedded `fetch`/`XMLHttpRequest`/`.ajax(` calls

```bash
grep -noE 'fetch\([^)]{0,80}|XMLHttpRequest|\.ajax\(' <file>.html
```

Minified bundled libraries (dayjs, React, etc.) often contain the string `fetch(` internally without ever calling it against a real endpoint — that's fine. What to actually look for: a call with a literal URL or relative path argument (e.g. `fetch('/api/...')` or `fetch('https://...')`). That indicates the artifact expects to talk to a live backend, which will not exist once served from a static CDN — flag it, don't ship it silently.

## When this applies

Run all three checks before:
- Adding a new file to `public/documents` (or the `artifact-collection-public` repo)
- Registering it in `lib/artifacts.ts` / the manifest
- Regenerating or re-exporting an existing artifact from another tool
