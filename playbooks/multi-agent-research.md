# Playbook — designing multi-agent research that is actually diverse

Written 2026-08-27 after a correct criticism: the research fleet was not diverse. Fourteen agents
ran, and **all fourteen did the same job** — search, fetch, summarise, return. Same method, same
failure mode, same blind spots. Diversity of *topic* is not diversity of *method*.

## The four failures of the fleet as it was

1. **Single perspective per question.** One agent, one brief, one answer, taken as true.
2. **Collection, not falsification.** Every prompt said "find X." **None said "kill this thesis."**
3. **No verification layer.** Nobody checked anyone. An agent's error became my belief.
4. **My framing embedded in every brief.** Two false premises — the 2026 state elections and the
   windfall tax — survived until one agent happened to challenge them
   ([[india-policy-calendar-and-two-corrections]]). That was luck, not design.

## The seven archetypes

Send **at least three different archetypes at any question that matters.** Never three of the same.

### 1. The Collector
What exists. Numbers, dates, sources. The only archetype the fleet used.
> "Find every published figure for X. Table it with source URL and date. Do not interpret."

**Use for:** establishing the factual floor. **Never use alone.**

### 2. The Falsifier (red team)
Its only job is to **destroy a thesis I hold**. Not to evaluate — to attack.
> "I believe [thesis]. Your job is to destroy it. Find the strongest disconfirming evidence, the
> best counter-argument, and the specific scenario in which someone holding this loses badly.
> Assume I am wrong and work out why. **Do not present a balanced view — argue the opposite case
> as forcefully as the evidence allows**, then state honestly how strong that case actually is."

**Use for:** every position before adding to it. This is the archetype I never once deployed.

### 3. The Steelman
Argues the case I have *rejected*, as strongly as possible.
> "I have dismissed [X] because [reasons]. Build the strongest possible case that I am wrong.
> What would someone who disagrees with me know that I do not?"

**Use for:** anything closed or benched — the ideas most likely to be closed for bad reasons.

### 4. The First-Principles Reasoner
**Forbidden from searching.** Reasons from stated facts to conclusions.
> "Do not search. From these facts alone [list], reason out what must be true, what cannot be
> true, and what is undetermined. Show the chain. Flag every step where you need a fact you do
> not have."

**Use for:** breaking out of the consensus that search results encode. Search returns what has
been written; this returns what follows.

### 5. The Verifier
Checks another agent's output, adversarially.
> "Another analyst produced [claims]. Independently verify each. For each: CONFIRMED with source,
> CONTRADICTED with source, or UNVERIFIABLE. **Do not accept a claim because it is plausible.**
> Flag anything with only one source, anything where the source is an aggregator quoting another
> aggregator, and any figure that cannot be traced to a primary document."

**Use for:** anything that will change a position. **This is now mandatory before any close or add.**

### 6. The Base-Rate Finder
How often does this pattern actually resolve the way I expect?
> "Find historical instances of [pattern]. For each: what happened next over 3, 6, 12, 24 months.
> Give the **distribution, not the average** — I need the failure cases as clearly as the successes.
> How many times did it resolve the way the consensus expected?"

**Use for:** any thesis resting on "this usually leads to that."

### 7. The Second-Order Thinker
What does this imply that nobody has priced?
> "Given [established fact], what are the second- and third-order consequences? Who is hurt that
> nobody is discussing? What is the non-obvious beneficiary? What breaks two steps downstream?"

**Use for:** turning a fact everyone has into a view nobody has. The memory-shortage-hits-Dixon
finding came from this shape ([[memory-shortage-is-a-tax-on-device-makers]]) — but by accident,
not design.

## Rules for writing any brief

- **Put my premises in the question, not the framing.** Never "given that X, find Y." Always
  "is X true, and if so what follows?" An agent that inherits an assumption researches around it.
- **Demand the distribution, not the point estimate.** "What is the range and what does the tail
  look like" beats "what is the number."
- **Require an explicit confidence tag per claim** — verified / reported / degraded / not found.
- **"Not found" must be stated, never estimated.** And it means *not retrieved*, not *does not exist*.
- **Require source URLs, not just dates.** The audit found **1,197 numeric claims and 0 URLs**
  across the base — traceable in time, not linkable to anything. That is the single biggest
  quality defect in this workspace.
- **Tell them what I already believe, and invite them to contradict it.** The cost of an agent
  politely confirming me is higher than the cost of a wrong challenge.
- **Pass down the house rules**: no artifacts without asking; caveman mode does not apply to
  subagent output.

## Budgeting

WebSearch is capped at **200 calls per session, shared across every agent**
([[research-budget-constraints]]). A deep agent uses 15-45. **That is five to eight agents, not
fourteen.** Launch in waves, and when the cap binds, **cut the Collectors first — they degrade
most gracefully. Keep the Falsifiers and Verifiers**, because judgement work is what the numbers
cannot replace.

**And: a rejected agent launch is an open task.** Five were dropped on 2026-08-26 for hitting the
concurrency cap. One was the governance screen. Its absence closed HDFC Bank
([[i-never-ran-governance-on-my-own-book]]).
