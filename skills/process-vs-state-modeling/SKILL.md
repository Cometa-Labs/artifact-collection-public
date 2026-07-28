---
name: process-vs-state-modeling
description: Design or clean up a pipeline/workflow model by strictly separating processes (the "-ing" activities, e.g. Qualifying, Onboarding) from states (the nouns/stages a subject is in, e.g. Candidate, Active). Use whenever a workflow, pipeline, or stage-based system's terminology is ambiguous or mixes activity and status into the same field.
---

# Process-vs-state modeling

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes a modeling technique originally described for VC deal-flow pipelines (Leads → Networking → Opportunity → Qualifying → Candidate → Committing → Investment → Monitoring & Reporting → ROI), but the process/state split applies to any staged workflow: hiring, sales, support ticketing, editorial review, grant review, etc.

## The core distinction

In an abstract pipeline, alternate between two kinds of things:

- **Processes** are activities — the "-ing" words (or their nominalized form, e.g. "Qualification"). They are things the organization *does*. They take time and consume effort, and they are usually where the interesting operational detail lives (who's responsible, what the checklist is, how long it typically takes).
- **States / concepts** are nouns — they describe what stage a subject is currently in as a result of a process completing. They are the things you'd filter a dashboard or report by.

A working pipeline alternates state → process → state → process → ... A state is what you're in; a process is how you got to the next state.

## Procedure

1. **List every term currently used to describe your workflow's stages.** For each one, classify it strictly as a process or a state. If a term does both jobs (e.g. "In Review" used as both a filter and a task name), that's a modeling smell — split it into the state ("Under Review") and the process that produces the next state ("Reviewing").
2. **Draw the pipeline as an alternating sequence**: state → process → state → process → ... Every state should have exactly one process that can move a subject out of it (the process may itself branch to multiple next-states, e.g. approved vs. rejected, but the *process* stays singular).
3. **Resist adding a "rejected" or "stalled" state to the base model** unless your domain genuinely requires tracking why something stopped. A subject can simply stop being promoted — not every workflow needs an explicit terminal-failure state. Add states like "watchlist" or "follow up later" only as deliberate extensions once the base pipeline is validated, not by default.
4. **Check that processes, not states, own the operational detail** — checklists, responsible parties, typical duration, and triggering conditions belong on the process, not the state. States should be simple enough to use as filter/report dimensions.
5. **Validate against a worked example**: pick one real subject and narrate it through every state and process by name. If you can't name the process that moved it from one state to the next, the model is incomplete.

## Output shape

- A two-column table: Processes (activities) vs. States/Concepts (nouns), pulled from your actual domain vocabulary.
- The pipeline drawn as an alternating state → process → state sequence.
- One worked example narrating a real subject through the full sequence.
