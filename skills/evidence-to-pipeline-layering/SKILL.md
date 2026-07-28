---
name: evidence-to-pipeline-layering
description: Structure an organization's data model into 5 traceable layers — raw evidence, extractions/interpretations, operational facts, pipeline stage records, and pipelines — so that business decisions stay human-controlled and traceable back to source evidence. Use when designing a data model or system architecture for any evaluation/decision workflow (deal flow, hiring, sales, research triage, grant review) that needs to go from unstructured source material to structured, auditable decisions.
---

# Evidence-to-pipeline layering

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes a 5-layer model originally described for VC deal-flow operations, but the layering applies to any organization that must evaluate things (companies, candidates, leads, submissions, cases) using a mix of unstructured source material and structured, human-approved decisions.

## When this pattern fits

Reach for this whenever you're designing how an organization's data should flow from "raw stuff we collected" to "a decision we can defend later," and you want:

- traceability from any decision back to the evidence that justified it
- room for disagreement/reinterpretation without destroying history
- a clean boundary between "material that describes reality" and "business logic that acts on it"

It does not fit workflows with no evidentiary or interpretive step — e.g. a purely mechanical/deterministic pipeline with no human judgment layer doesn't need this scaffolding.

## The five layers

1. **Layer 0 — Evidence.** Immutable source material: recordings, emails, messages, documents, images, archived pages, logs. Never edit in place; this is the record of what actually happened or was said. Interactions are a common subset of evidence but not the only kind — documents and archived material count too.

2. **Layer 1 — Extractions & Interpretations.** Authored notes or generated outputs derived from evidence: summaries, transcriptions, OCR, observations, insights. This layer is explicitly observer-dependent — different people or models can produce different interpretations of the same Layer 0 evidence, and that's expected, not an error to resolve.

3. **Layer 2 — Operational Facts & Canonical Statements.** Structured, machine-readable statements synthesized from Layer 1: normalized facts, current believed conclusions, tentative/disputed statements, approved/signed-off statements. This is the last upstream layer before business logic begins — it's where the org decides what it currently believes to be true, with room for a fact to be tentative or later disputed.

4. **Layer 3 — Stage Records.** A record of a specific subject being evaluated at one process stage: checklist-driven, human-triggered, can prefill from Layer 2, supports a proceed/no-proceed decision. This is where business logic actually starts. Use a reevaluation model rather than in-place edits: freeze the old row, generate a new row when re-evaluating, and flag the frozen row as potentially stale when new upstream data arrives.

5. **Layer 4 — Pipelines.** The highest-level, executive-facing business logic: composed of Layer 3 stage records, human-defined, and implemented as concrete campaigns/instances. This is the layer the organization actually talks about day to day (e.g. "deal flow," "candidate pipeline").

## Procedure

1. **Identify the subject(s) being evaluated** in your domain — the equivalent of "investable subject." Confirm whether a subject is always a single entity or can be a structured combination (e.g. founder + project, candidate + role) — don't assume single-entity if the domain has meaningful combination cases.
2. **Map your existing data/artifacts onto the five layers** before designing anything new. Most orgs already have Layer 0 (source material) and some ad hoc Layer 1 (notes); the usual gap is a missing Layer 2 (nobody owns "what do we currently believe is true") and a Layer 3/4 split (stage-level records vs. the pipeline that composes them are conflated into one thing).
3. **Enforce the boundary**: nothing below Layer 3 should encode a proceed/no-proceed decision. If you find business logic leaking into Layer 1 or 2, that's a sign the model is under-layered.
4. **Design Layer 3 as append-only per stage**, not editable in place, so a subject's evaluation history at each stage is fully reconstructable.
5. **Design Layer 4 pipelines as reusable templates**, separate from any specific run — see [[pipeline-vs-campaign-pattern]] for how to split "the reusable definition" from "one real run of it."

## Output shape

- A layer table: layer number → what it is → example artifacts in your domain → who/what produces it.
- An explicit statement of where the business-logic boundary sits (top of Layer 2 / bottom of Layer 3).
- A note on the reevaluation model for Layer 3 (freeze + new row + staleness flag).
