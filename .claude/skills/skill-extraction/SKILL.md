---
name: skill-extraction
description: Extract a reusable agent skill from a single HTML document in the artifact-collection-public docs repo, through a discovery pass followed by a user interview, then write it as a real skills/<slug>/SKILL.md folder and register it in skills/manifest.json. Use whenever the user wants to "extract a skill" from a document, turn a report/analysis into a reusable playbook, or asks what skill a specific artifact contains — always after a document has already been published, never before. Do not skip straight to writing a skill file from a quick read of the document; discovery only produces candidates, and every candidate must go through the interview stage before anything is written.
---

# Skill extraction

Turns one already-published document in `artifact-collection-public` into a real, reusable skill folder — not just a metadata row. This is a two-stage process on purpose: a document usually contains one specific worked example, and a skill needs to generalize past that one example without inventing claims the document doesn't support. The discovery stage separates "does this document contain a repeatable procedure at all" from "what exactly should the skill say" — the second question needs the user, not just the document.

Scope: **one document per run.** Don't scan the whole corpus looking for cross-document skills — if the user wants that, they'll ask for it explicitly. Most documents (pure reports, one-off market maps, calculators) don't contain an extractable skill at all, and that's a fine outcome — say so and stop rather than forcing something.

## Stage 1: Discovery

1. Read the target document in full (fetch its raw content — see `references/fetching-documents.md` for how documents are proxied vs. served raw).
2. Ask: does this document describe a **repeatable procedure** — a method, a checklist, a way of reading/classifying/computing something that would apply to other inputs of the same shape — or is it a **one-off finding** (a specific conclusion, a snapshot, a single number)? Only the former is skill material. A document can contain zero, one, or occasionally more than one candidate.
3. For each candidate found, write a short pitch (name + one sentence on what repeatable thing it does) — don't draft the full skill yet. Present all candidates to the user together and ask which (if any) to proceed with. If discovery finds nothing extractable, say that plainly and stop — don't manufacture a skill from a document that's just a report.

## Stage 2: Interview

For each candidate the user wants to pursue, don't fill in the schema from guesswork — ask. In particular:

- **Scope check**: does the document's specific example generalize the way you assume, or is the user narrowing/widening it? (E.g. a worked trace on one protocol's transactions — does the skill apply to that protocol specifically, or to a class of similar protocols?)
- **`category`**: which of `Research | Operations | Market | Product | AI` fits, if the document doesn't make it obvious.
- **`whenToUse`**: confirm the trigger condition in the user's words, not just a paraphrase of the doc's topic sentence.
- **`inputs` / `outputs`**: the document usually only shows one worked input/output pair — confirm what varies across other uses of this skill.
- **`relatedArtifacts`**: confirm which published documents (by slug) this skill should link back to — usually at least the source document, sometimes more.
- **Anything the document leaves ambiguous or you had to infer** — surface it and ask rather than silently deciding. If the user isn't available to answer, write the skill with your best inference but flag every inferred field explicitly in your summary back to them before publishing.

Never skip this stage because a candidate "seems obvious" — the interview is what keeps the skill honest about what's actually generalizable versus what you're assuming.

## Writing the skill

1. Pick a slug: kebab-case, unique against the existing `skills/manifest.json`, and an `indexCode` following the same `<PREFIX>-<3-digit-number>` global-sequential convention documents use (see the docs repo's `references/skills-schema.md` if working from the bootstrap package, or just find the highest existing `SKILL-NNN` and increment).
2. Write `skills/<slug>/SKILL.md`: real frontmatter (`name`, `description` — pushy, states both what it does and when to trigger), then a body that states the generalized procedure the interview converged on. Ground every step in what the source document actually showed; don't pad with generic advice the document doesn't support.
3. **Every skill file this process produces must open with this caveat**, verbatim or close to it, right after the frontmatter:
   > Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.
4. Add the metadata to `skills/manifest.json` (`slug`, `name`, `indexCode`, `category`, `summary`, `whenToUse`, `inputs`, `outputs`, `relatedArtifacts`, `tags`) — every field sourced from the interview, not invented.
5. If working inside the `artifact-collection-public-bootstrap` package, use its `scripts/validate_skills_manifest.py` to validate before committing. If this skill was installed standalone (not via bootstrap), validate by hand: unique slug, unique indexCode, valid category enum, and confirm `skills/<slug>/SKILL.md` exists on disk.
6. Commit and push the same way documents are published (see the docs repo's own publish instructions) — including a jsDelivr purge for `skills/manifest.json` and the new skill's files if immediate visibility matters.

## What this skill does not do

It doesn't touch `documents/manifest.json` or the original document — extraction is additive. It doesn't re-open the publishing-clearance question for the source document (that already happened when the document itself was published) — but if the interview surfaces something in the *generalized* skill that goes beyond what was cleared for the original document (e.g. broader claims, different audience), flag that to the user rather than assuming it's covered.
