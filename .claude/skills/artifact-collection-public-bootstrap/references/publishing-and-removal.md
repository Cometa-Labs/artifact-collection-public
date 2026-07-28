# Publishing clearance and removal limits

This repo is public. Both directions of that fact need explicit handling: what has to be true *before* something goes in, and what "taking something out" actually does (and doesn't do) once it's been public even briefly.

## Before publishing: clearance gate

Before adding any item to `documents/manifest.json` and pushing, confirm with the user that the document has been cleared by legal or a team lead to be made public. Don't assume silence or eagerness to ship means clearance was obtained — ask directly if it hasn't come up. This is step B.1 in `SKILL.md` for a reason: it comes before the audit, before writing the manifest entry, before anything else, because everything downstream is much easier to undo than the publish itself.

Why this gate matters more here than in a typical "add a file to a repo" workflow: once pushed to `main`, the content is fetched by jsDelivr's CDN and can be viewed by anyone with the raw URL within seconds — there's no staging, no review gate, no access control between "committed" and "publicly served."

## After publishing: what removal actually does

Removing an item means: delete its entry from `manifest.json`, delete its `.html` file, commit, push, and (optionally) purge the jsDelivr cache. That stops the consuming app from listing or serving it going forward. It does **not** erase the fact that it was public. Specifically, once something has been pushed to `main` on a public repo, assume it is permanently and irrevocably available somewhere, because:

- **Git history retains it.** The file's full content lives in every commit before the removal commit. Anyone can `git log`, check out an old commit, or browse GitHub's commit history UI and read it — deleting the file in a new commit does not touch the old one.
- **Forks and clones keep their own copy.** Since the repo is public, anyone could have already forked or `git clone`d it before removal, with no way for you to reach into their copy.
- **jsDelivr caches commit-pinned URLs indefinitely.** A URL like `.../artifact-collection-public@<commit-sha>/documents/<file>.html` (as opposed to `@main`) is treated as immutable by jsDelivr and may be served forever, by design — that's a separate, permanent path to the same content regardless of what `main` looks like now.
- **The `@main` CDN cache itself** may still serve the old content for up to ~12-24h even after a purge request, and browsers/proxies in between may have their own caches on top of that.
- **Search engines and archival crawlers** (Google, Bing, the Wayback Machine, etc.) index public GitHub content and raw CDN URLs independent of anything this repo's maintainers control, and don't reliably honor deletions after the fact.

**Bottom line:** treat "remove from the knowledgebase" as "stop distributing going forward," not "erase." If something genuinely sensitive was published (PII, a real secret, something legal explicitly needs pulled), that's a disclosure incident — loop in the user/legal about it directly rather than treating a `git rm` + push as having resolved it. Rewriting git history (`git filter-repo`/BFG) and force-pushing is a real but heavyweight option for that scenario specifically; it does not reach anyone who already cloned or forked before the rewrite, and should be a deliberate decision made with the user, not something done automatically as part of a routine removal.
