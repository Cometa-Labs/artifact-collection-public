---
name: junior-vs-senior-cost-framework
description: Compare junior vs senior (or any two-tier) hires on cost-per-unit-of-output rather than raw salary, by walking through the same four levers every time — capacity ramp toward full productivity, quality/rework penalty, sustainable hours, and salary relative to market. Use when asked whether hiring junior or senior engineers (or a similar two-tier hiring/staffing decision) is more cost-effective, or why a cheaper hire isn't necessarily cheaper per unit of output.
---

# Junior-vs-senior cost framework

> Auto-generated from open-domain document content and provided as-is. Not tested, and not necessarily a skill Cometa Labs uses in its own workflows. Treat the specific formula in the source document as illustrative, not a validated model — the durable part is the four-lever framework, not the exact math.

This skill generalizes the structure of a junior-vs-senior cost-per-output model: rather than comparing salaries directly, it decomposes "cost per unit of shipped output" into four independent levers, so a cheaper hire can be shown to be more or less cost-effective depending on where those levers land — not just on headline salary.

## The four levers

1. **Capacity ramp toward full productivity.** A hire's effective capacity isn't fixed — it depends on how much you're paying relative to market (paying under market yields under-full capacity; paying at/above a full-activation threshold yields full capacity). Junior and senior hires can have different ramp curves and different maximum capacities even at full activation — a junior at full capacity may still cap out below a senior's baseline.

2. **Quality / rework penalty.** Output isn't just volume — a higher bug/rework rate effectively divides raw output, since defective work has to be redone. This penalty is usually not equal between tiers, and is one of the more important levers because it can flip which tier is actually cheaper even when raw hours and salary look favorable to the "cheap" hire.

3. **Sustainable hours.** Don't assume both tiers work the same hours. One tier may have a wider or narrower range of sustainable/overtime hours before diminishing returns or burnout — model this explicitly rather than assuming a flat 8-hour day for both.

4. **Salary relative to market, not absolute salary.** What you pay matters relative to each tier's own market rate, not as a raw number — a senior paid below their market rate and a junior paid above theirs are both being mispriced relative to the activation curve in lever 1, which changes their realized capacity.

## Procedure

1. **Name your two (or more) hiring tiers** and, for each lever above, write down your actual assumption in plain language before doing any math — e.g. "junior tops out around 60% of senior capacity even when fully ramped," "junior bug rate is roughly 2.5x senior's." If you don't have real data for a lever, say so and treat that number as a sensitivity input, not a fact.

2. **Compute (or estimate) net output per tier** as capacity × hours, discounted by the rework penalty — output isn't raw hours worked, it's hours worked that actually stick.

3. **Compute cost per unit of output** as salary ÷ net output for each tier, not salary alone. This is the number that actually answers "which is cheaper," and it can invert the naive salary comparison.

4. **Stress-test the conclusion against the levers**, not just the headline numbers — identify which one or two levers the conclusion is most sensitive to (usually capacity ramp and rework penalty dominate) and say so explicitly, so the reader knows what assumption to challenge if they disagree with the result.

5. **State the result as conditional on the assumptions**, not as a universal fact — "under these capacity/bug-rate/hours assumptions, X is cheaper per unit of output" — and name the lever that would flip the conclusion if it moved.

## Output shape

- A four-lever assumption table: lever → tier A value → tier B value → source/confidence.
- Net output and cost-per-output for each tier.
- One sentence naming which lever(s) the conclusion is most sensitive to.
- The conclusion stated conditionally, with the flip-condition named.
