# Fetching a document's raw content for extraction

To read a document during the discovery stage, fetch its raw text directly — you don't need a browser or an iframe, just the bytes:

```bash
curl -s "https://cdn.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/<file>.html"
```

Note: jsDelivr serves `.html` files here as `Content-Type: text/plain` (deliberately — it won't host arbitrary HTML as an executable page under its own domain). That's irrelevant for extraction purposes since you're reading it as text, not rendering it in a browser; it only matters for the consuming app's iframe viewer, which proxies through `/api/docs/[file]` to fix the content-type for rendering. Don't worry about it here.

If the document is large or has a lot of markup noise, strip tags before reading for content (keep an eye out for embedded `<script>` bundles — those are usually a minified library, not content worth reading):

```bash
curl -s "https://cdn.jsdelivr.net/gh/Cometa-Labs/artifact-collection-public@main/documents/<file>.html" \
  | python3 -c "import sys, re; h = sys.stdin.read(); h = re.sub(r'<(script|style).*?</\1>', ' ', h, flags=re.S); print(re.sub(r'<[^>]+>', ' ', h))"
```

The document's own manifest entry (`documents/manifest.json`) is also worth reading first — its `summary` and `agentUse` fields are a fast way to judge whether a document is even a plausible discovery candidate before pulling the full HTML.
