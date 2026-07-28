# What a valid `.html` artifact looks like

Every file in `documents/` is served as-is from a GitHub-backed CDN (jsDelivr) and rendered directly in an `<iframe>` by the consuming app. There is no build step, no bundler, and no server-side templating between the file in this repo and what the end user sees. That gives two hard constraints:

1. **Fully self-contained.** No external `<script src>`, `<link href>`, web fonts, or images hosted outside the file itself. Inline everything: `<style>` blocks for CSS, `<script>` blocks for JS, data URIs or inline SVG for images. If a library is needed (charting, date formatting, etc.), the minified source is pasted directly inside a `<script>` tag — not loaded from a CDN `<script src>`. This is what makes the file portable to jsDelivr without breaking: jsDelivr serves the raw bytes of exactly this file, nothing else resolves relative to it.
2. **No live backend dependency.** The file cannot `fetch()`/XHR a real API at render time — there's no origin of its own to authenticate against, and the consuming app's origin is different from the CDN's. Any data the page needs must be baked into the HTML at authoring time (inline `<script>` with a data object, or literal values in the markup).

Plain outbound `<a href="https://...">` citation links that a human clicks are fine and common (e.g. sourcing a claim). Those are not page dependencies — they just need `rel="noopener noreferrer"` whenever they carry `target="_blank"` (see the audit section of `SKILL.md`).

## Minimal skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Artifact Title</title>
  <style>
    :root { color-scheme: light; }
    body { font-family: system-ui, sans-serif; margin: 0; padding: 2rem; line-height: 1.5; }
    h1 { font-size: 1.5rem; }
    a { color: inherit; }
  </style>
</head>
<body>
  <h1>Artifact Title</h1>
  <p>Body content goes here. Everything the page needs — styles, scripts, data — lives inside this one file.</p>

  <p>
    Source:
    <a href="https://example.com/source" target="_blank" rel="noopener noreferrer">example.com</a>
  </p>

  <script>
    // Any interactivity is self-contained inline JS. No external <script src>,
    // no fetch() to a live API — bake data in as a literal object if needed.
    const data = { rows: [/* ... */] };
  </script>
</body>
</html>
```

See `assets/example-artifact.html` for a runnable copy of this skeleton to start a new artifact from.

## Interactive artifacts (calculators, designers, etc.)

Some existing artifacts (e.g. the token-tier calculator, the gacha machine designer) bundle a full minified JS framework inline — that's expected and fine, as long as the bundle itself makes no network calls to a real endpoint. When auditing one of these, a `fetch(` match inside a minified library blob (dayjs, React, etc.) that never resolves to a literal URL argument is not a violation — see the audit section for how to tell the difference.
