---
name: pipeline-vs-campaign-pattern
description: Split a reusable process definition (a "pipeline") from its implemented, real-world runs (a "campaign") so the same process template can be instantiated repeatedly against different cohorts, themes, or sourcing efforts without redefining it each time. Use when a team keeps redefining "how we do X" from scratch for every new batch/cohort/initiative instead of running a shared template.
---

# Pipeline-vs-campaign pattern

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes a distinction originally described for VC operations (the "venture-backed company pipeline" vs. "Spring 2026 Pitch Competition Cohort" as one campaign that implements it), but it applies to any org running the same structured process repeatedly against different real-world instances.

## The core distinction

- **Pipeline** — a reusable business process definition. It describes how a *class* of subjects should move through a shared abstract lifecycle (e.g. lead → opportunity → candidate → committed outcome). It is not tied to any specific batch, event, or time period.
- **Campaign** — an implemented pipeline: one real operational instance, tied to a specific cohort, theme, event, thesis, or sourcing effort. A campaign uses a pipeline's definition but has its own subjects, timeline, and outcomes.

`Pipeline = reusable business process definition. Campaign = implemented instance of that pipeline.`

## When to apply this split

Apply it when you notice a team repeatedly reinventing the stages, checklist, or criteria for "how we evaluate X" every time a new batch of X shows up — a strong signal the process definition and the specific run are tangled together in one artifact instead of separated.

## Procedure

1. **Extract the pipeline**: write down the stages, criteria, and decision points that should stay constant across every run of this process, independent of which subjects are currently in it or when it's running.
2. **Confirm the pipeline is genuinely reusable**, not a one-off dressed up as a template — ask whether you can name at least one other real or plausible campaign that would use the exact same pipeline definition. If not, it may just be a single campaign; don't force the split prematurely.
3. **Define what a campaign adds** on top of the pipeline: a name/theme, a time window, a specific set of subjects (a cohort or sourcing effort), and any campaign-specific parameters (e.g. a different qualification bar for a specific event) — while keeping the underlying stage sequence identical to the pipeline.
4. **Allow multiple simultaneous campaigns** against the same pipeline (e.g. two concurrent cohorts both running the same evaluation process) and multiple pipelines for meaningfully different subject classes (don't force every subject type through one universal pipeline if the class-level criteria genuinely differ — see [[evidence-to-pipeline-layering]] for how stage records under a pipeline should be structured).
5. **Route pipeline changes deliberately**: a change to the pipeline definition affects every future campaign that uses it; a change scoped to one campaign should not leak back into the shared pipeline definition. Keep these two change types visibly distinct in however you version or document the process.

## Output shape

- A one-paragraph pipeline definition (stages + criteria), free of any reference to a specific batch/date/cohort.
- A short list of campaigns that instantiate it, each with its own name/theme/time window/subject set.
- A flag for any pipeline-vs-campaign coupling found during extraction (i.e. process detail that was hardcoded into one campaign but actually belongs in the shared pipeline).
