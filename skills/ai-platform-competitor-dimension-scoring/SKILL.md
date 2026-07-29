---
name: ai-platform-competitor-dimension-scoring
description: Map the competitive landscape of AI/LLM infrastructure platforms (routers, gateways, multi-model chat apps, workflow/agent platforms) by scoring each on bipolar dimensions (with a stated "why it matters" per dimension), grouping by platform category, and reading the resulting matrix for open positioning space. Use when asked to build a competitor map or positioning analysis for AI model routers, LLM gateways, inference platforms, multi-model chat apps, or agent/workflow platforms.
---

# AI platform competitor dimension scoring

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows.

This skill generalizes the competitor-mapping method used across 25 AI infrastructure platforms (OpenRouter, Requesty, Portkey, LiteLLM, Groq, Together, CrewAI, Masumi/Sokosumi, etc.) spanning four platform categories: router/aggregator, infra/vertical-stack owner, multi-model chat app, and workflow/agent platform.

## Procedure

1. **Sort candidates into the four platform categories first**, before scoring anything: router/aggregator (sits between caller and model providers), infra/stack owner (owns compute or a vertical stack), multi-model chat app (consumer/prosumer-facing chat UI over multiple models), workflow/agent platform (sells outcomes or automations, not raw inference). A platform's category is often more explanatory than any individual dimension score — note it before you start scoring, and use it as the plot's color/shape encoding later.

2. **Define 6-10 bipolar dimensions relevant to this category**, each with a low pole, a high pole, and a one-line "why it matters" — the reason a buyer or the business would care about this axis at all, not just what it measures. A dimension without a stated "why it matters" tends to get scored inconsistently, because different scorers silently disagree on what the axis is actually proxying for.

3. **Use half-point scores (1-10, allowing .5) deliberately** to prevent platforms from stacking on top of each other when plotted — ties in the underlying data are real, but visual overlap hides distinctions worth surfacing (e.g. "these two are both roughly here, but one is slightly ahead").

4. **Score from direct product research** (pricing pages, FAQ, docs, product UI) and always distinguish self-reported claims from a competitor's own marketing versus third-party or your own direct observation — an overhead/margin number published by a company comparing itself favorably to competitors is directional, not audited; say so in the note, don't launder it into a clean score.

5. **Cross-reference dimension scores against a feature-importance-by-category table** if you're also cataloging concrete features: which dimensions are table-stakes (every platform in a category needs it, so it stops differentiating) versus genuine differentiators (only some platforms have it, and it still moves buyer decisions) versus not-yet-relevant for that category. A dimension where everyone scores high is no longer a useful axis for finding whitespace — say so explicitly rather than plotting it anyway.

6. **Read the matrix for structural gaps**, not just the highest/lowest scorer per dimension — the strongest finding is usually "no platform combines high scores on dimension A and dimension B simultaneously" (e.g. nobody owns both compute margin and workflow depth). State that gap as the headline finding, with the specific platforms nearest to each pole as evidence.

## Output shape

- Category assignment per platform (router/infra/chat/workflow or your category set).
- Dimension table: # → dimension → low pole → high pole → why it matters.
- Score matrix: platform × dimension, half-points allowed, with a source note (direct observation vs. self-reported) per score.
- Feature-importance-by-category table if features were also cataloged (must-have / differentiator / optional / not relevant, per platform category).
- One stated structural gap: the dimension-pair combination no current platform occupies, and why that's a positioning opportunity.
