---
title: "ICLR 2026: Memory Is the Substrate"
subtitle: "What I Took From Rio: AI Is Shifting From Models That Answer to Systems That Maintain State"
date: 2026-04-29
categories: [startups]
tags: [ai, agents, memory, iclr, world-models, rsi, evaluation, harness, policy]
canonical_url: "https://x.com/hammadtariq/status/2049366514411643049"
author_profile: false
related: false
share: false
toc: true

header:
  teaser: /assets/images/iclr-2026-rio-ipanema.png

sidebar:
  nav: "categories"
classes: "wide"

summary: "I came to ICLR looking for memory systems. I left thinking memory is only one part of a bigger shift — the field is moving from models that answer to systems that maintain state, act, evaluate themselves, and improve over time."
---

![Ipanema at sunset, Rio de Janeiro — ICLR 2026.](/assets/images/iclr-2026-rio-ipanema.png)
{: .align-center}

I came to ICLR looking for memory systems.

I left thinking memory is only one part of a bigger shift.

The field is moving from models that answer to systems that maintain state, act, evaluate themselves, and improve over time.

That is the signal I took from Rio.

## 1. The model is no longer the whole product

One of the clearest patterns was that the harness is becoming a first-class object.

In the industry talks, this was obvious. Zillow's agent architecture was not presented as "we call an LLM and hope it works." It was a full agent harness: knowledge layer, action layer, user understanding, skills, sub-agents, planning, memory, policy, and execution loops.

The LLM was swappable.

That is the important part.

GPT, Claude, open-weights — they plug into the system. The system is the thing being engineered.

This same pattern appeared in research.

AutoHarness is literally about generating code harnesses around agents. Instead of only improving the model, it improves the wrapper that constrains, guides, and executes behavior.

ADAS — Automated Design of Agentic Systems — pushes this further: define the agentic-system search space in code, then let AI search for better agent architectures.

That is a different mental model.

## 2. RAG is becoming too small a word

RAG retrieves chunks.

Memory maintains state.

That distinction kept coming up again and again.

A lot of the memory work at ICLR was not just "retrieve more context." It was trying to answer deeper questions:

- What should be remembered?
- What should be compressed?
- What should be forgotten?
- What should be retrieved now?
- What should become persistent state?
- What evidence supports a memory?
- How does memory change over time?

**AssoMem** framed memory as associative retrieval, not just semantic similarity. The point is simple: cosine distance is not enough. Human memory links things through time, importance, relevance, context, and association.

**MEM1** pushed the same idea from another angle: long-horizon agents cannot just append all past turns forever. They need a compact internal state that helps memory and reasoning work together.

**Limited Memory Language Models** externalized factual knowledge into a database during pretraining instead of burying everything inside opaque weights.

**Evoking User Memory** split retrieval into something closer to human cognition: fast familiarity and slower recollection.

**HippoRAG** and the **MemAgents** talks kept coming back to a biological intuition: memory is not a pile of text. It is an active mechanism for finding, linking, and using past experience.

## 3. Memory is becoming part of self-improvement

The most interesting version of memory is not passive.

It is not just:

> store → retrieve

It is:

> experience → reflect → update memory → retrieve better next time → improve behavior

That is where memory and recursive self-improvement start to touch.

Jeff Clune's MemAgents keynote made this explicit. His talk connected memory to a much broader open-endedness agenda: POET, AI-generating algorithms, OMNI-EPIC, ADAS, HyperAgents, ALMA, and The AI Scientist.

The strongest pattern was not "AI improves itself" in some vague sci-fi sense.

It was more concrete: **automate the search over systems.**

- Search over environments.
- Search over curricula.
- Search over agent architectures.
- Search over memory designs.
- Search over scientific hypotheses.

**ALMA** was the cleanest memory-specific version of this. The premise is blunt: most memory systems are hand-designed, fixed, and brittle. ALMA tries to meta-learn memory designs for agentic systems.

That is a big idea.

Not:

> we built a better memory module

But:

> the memory architecture itself can be searched over and improved

That feels like a real direction.

## 4. RSI is becoming boring in a good way

Recursive self-improvement used to sound like a philosophical argument.

At ICLR, it felt more like systems engineering.

There is no single RSI loop. There are many loops:

- code improves
- prompts improve
- memory improves
- tools improve
- data improves
- evaluators improve
- policies improve
- weights sometimes improve

That is the grounded version.

The interesting systems are not necessarily self-improving end-to-end. They are improving some component inside a controlled loop.

This matters because "self-improvement" becomes much less magical when you ask:

**What exactly is allowed to change?**

- A prompt?
- A memory schema?
- A tool?
- A reward model?
- A policy?
- A dataset?
- A planner?
- A model checkpoint?

That is where the work is.

And the hard part is not just improvement. It is **safe** improvement.

- How do you prevent reward hacking?
- How do you prevent memory corruption?
- How do you know the system improved instead of overfitting the evaluator?
- How do you roll back a bad update?

That is where the next tooling layer will appear.

## 5. World models are about consistency, not just generation

World models were another major signal.

The shallow version is:

> generate future video

The deeper version is:

> maintain a consistent model of the world across time, action, and viewpoint

That is much harder.

The **ViewRope** world-model poster made this very concrete. The problem is not just making plausible frames. The problem is geometric consistency: if the camera moves, rotates, revisits a place, or closes a loop, does the world stay the same?

**Latent Particle World Models** attacked the problem from the object side: object-centric stochastic dynamics, particles, masks, actions, and goals.

These are different techniques, but the same direction: agents need stable internal state about the world.

That is why world models connect back to memory.

- Memory is state over experience.
- World models are state over environment.

Both are about preventing the system from drifting.

A model that cannot maintain state cannot plan well. A model that cannot test its state against reality cannot improve.

## 6. Science AI looked more real than I expected

The science work was better than I expected.

Not because it was flashy. Because it was constrained.

Hard domains force the model to prove something.

In science, you cannot just sound plausible. You need benchmarks, measurements, physical constraints, experiments, or domain-specific evaluation.

**AstaBench** was one example: benchmarking scientific research agents across actual research workflows.

The **protein binder** work was another: generative pretraining plus test-time compute for atomistic protein binder design.

**WIND** used diffusion for atmospheric modeling, but the interesting part was not "diffusion is cool." It was using a generative model under physical constraints and inverse-problem structure.

The **fMRI-to-image** paper was also memorable. The key idea was not just better image generation. It was fixing the first stage: mapping brain signals into a better latent representation before reconstruction.

That is the science pattern: the hard part is often the representation and evaluation layer, not just the generator.

This is why hard-science AI is interesting. It forces the stack to become real.

## 7. Safety and policy are part of memory

Another thing became clearer to me: if agents have memory, policy cannot be an afterthought.

A long-lived agent needs to decide:

- should this be stored?
- who can access it?
- when can it be retrieved?
- can it be shown to this user?
- should it expire?
- should it be forgotten?
- was it used correctly?

Zillow's fair-housing / inverse-constitutional-AI framing made this concrete. Static rules are brittle. Real policy boundaries are contextual. The same phrase can be okay in one context and problematic in another.

That means memory is not just storage. It is a **policy-gated read/write system.**

For enterprise agents, healthcare agents, real-estate agents, finance agents, personal assistants — this is not optional.

Persistent memory without access control, provenance, deletion, and policy is a liability.

So the next memory stack probably has three parts:

1. structured memory
2. retrieval/update policy
3. audit and governance

That is the product-shaped version.

## 8. The real convergence

The more I walked around ICLR, the more the same pattern kept reappearing under different names.

- Memory people were talking about retrieval, consolidation, state, and forgetting.
- Agent people were talking about harnesses, tools, evaluators, and planning loops.
- World-model people were talking about consistency over time.
- RSI people were talking about systems that update themselves.
- Science people were talking about evaluation, constraints, and closed loops.

These are not separate trends. They are converging.

The next AI stack looks something like this:

```
model
+ memory/state
+ tools/actions
+ policy gates
+ evaluators
+ world model
+ update loop
```

The model is still important. But the surrounding system is becoming just as important.

Maybe more important.

## What I think comes next

My bet after ICLR:

### 1. RAG turns into memory infrastructure

Basic retrieval becomes commodity. The interesting layer is persistent, structured, temporal memory with provenance, uncertainty, forgetting, and policy.

### 2. Agent harnesses become trainable

The harness will not just be hand-coded. It will be searched, optimized, learned, and improved.

### 3. Memory managers become learned systems

The next memory systems will decide what to store, compress, retrieve, and update.

Not every memory will be a chunk.

- Some will be facts.
- Some will be events.
- Some will be summaries.
- Some will be state.
- Some will be policies.

### 4. Evaluation becomes core infrastructure

If a system can improve itself, the evaluator becomes part of the product.

Bad evaluator, bad self-improvement.

### 5. World models and memory start merging

For embodied agents, scientific agents, enterprise agents, and personal agents, the system needs a stable model of what is true, what changed, and what might happen next.

That is memory plus world modeling.

### 6. Policy-gated memory becomes mandatory

The more useful memory becomes, the more dangerous it becomes.

Safe memory is not just "don't store sensitive things." It is contextual access, deletion, retention, provenance, and auditability.

## My takeaway

I left thinking the real direction is **stateful AI**.

The next wave is systems that:

- maintain state
- reason over time
- retrieve the right past
- act through tools
- evaluate outcomes
- update themselves
- and stay within policy boundaries

That is the frontier I saw in Rio.

If you are building, I would not build another thin wrapper around an LLM.

I would build the state layer.

Because once agents become long-lived, memory is not a feature.

**Memory is the substrate.**
