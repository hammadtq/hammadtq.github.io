---
title: "PageRank for the Agentic Web: Separating Authority from Selection"
date: 2025-12-27
categories: [startups]
tags: [agents, web, policy, delegation, openbotauth, standards]
author_profile: false
related: false
share: false
toc: true

sidebar:
  nav: "categories"
classes: "wide"

summary: "Agents will reshape how choices get made on the web. Authority and selection are two distinct layers that need to stay separate. Here's why that matters and what a portable selection policy might look like."
---

A couple of days ago, I tossed out a thread on X about what I'm calling "PageRank for the agentic web." It started simple: a user tells an agent, "buy 12 eggs, don't ask questions." Fine, but which eggs? Which brand, merchant, or SKU? Who decides the algorithm behind that choice?

The thread got me thinking deeper about how agents will reshape the web, and why we're conflating two critical layers that need to stay distinct.

The egg example isn't just cute. It's a proxy for the headless interfaces coming our way. Chat, voice, agents: browsing as we know it fades, and selection becomes the default power center. That's the "PageRank" analogy. In the old web, PageRank surfaced relevance amid information overload. Here, it's about surfacing choices amid action overload. But to get there, we have to split authority from selection cleanly.

### The Two Layers: Authority vs. Selection

Authority is about delegation and mandates. Can this agent act on my behalf? What about sub-agents it spins up? It's the trust chain that lets actions happen without constant human intervention.

Selection, on the other hand, is the "why this one?" layer. Constraints, preferences, incentives, audits. All feeding into why a particular SKU wins out. It's not ranking for its own sake; it's optimization under policy.

People keep mashing these together, but they're orthogonal. Authority enables the act; selection guides it. Mix them up, and you end up with brittle systems where trust breaks or choices get captured.

### Authority: Web Bot Auth and Delegation

Web Bot Auth (WBA) is tackling authority head-on. It's an IETF draft for standardizing bot identities and interactions, and we're building a reference implementation at openbotauth.org. The repo is open-source, with specs and prototypes to push neutrality and interoperability.

One direction I'm exploring is delegation and mandates. Right now, I'm prototyping an X.509 chained delegation token in this PR: [github.com/OpenBotAuth/openbotauth/pull/6](https://github.com/OpenBotAuth/openbotauth/pull/6). The idea is to profile X.509 for agent delegation, using chains to propagate authority from user to agent to sub-agent.

In simple terms: imagine a user grants an agent permission to buy groceries. The agent delegates to a sub-agent for payment processing. Without chained delegation, each hop requires re-authentication or custom trusts. With it, you get verifiable chains. Proof that authority flows legitimately. This matters before commerce or automation scales, because broken trusts mean exploits, denials, or just plain friction. It's foundational plumbing.

We've also got a WordPress plugin in the repo as a reference for publishers. It handles policy verification on the server side, letting sites enforce bot auth without reinventing wheels. Not a product, just a practical surface to test these ideas.

### Selection: The Missing "PageRank" Layer

Once authority is sorted, users won't just delegate actions. They'll delegate *how to choose*. That's "delegated agency" or "choice delegation." For the eggs: hard constraints like max spend or dietary needs (halal, organic), soft preferences like cheapest vs. fastest, and avoids like certain brands.

This isn't mere ranking. It's policy-driven optimization. Budget, delivery time, ethics, no substitutions. All layered in. Without a standard way to express this, agents default to their builders' biases, turning selection into a monopoly lever.

### Related Research on Selection

The problem of how agents select on behalf of users isn't new ground. Researchers have been exploring similar ideas in multi-agent systems.

AgentRank adapts PageRank concepts to agent ecosystems by blending usage frequency with competence metrics like quality and latency. It uses protocols to aggregate private signals without requiring a global graph. This is a direct analog to the "PageRank" problem I'm describing here, but shifted from web links to agent performance in a web-of-agents context.

Multi-agent delegation models without money explore how principals select from competing agents' signals, showing gains in utility from competition even with correlated preferences. This hints at incentive structures for selection, where agents vie under constraints rather than pure market dynamics.

My framing leans practical: standardize authority via WBA, then layer portable selection schemas that compile to existing engines. Avoid new silos.

### A Proposed Policy Schema for Selection

What if we framed selection as a portable policy schema? Something simple, JSON-ish, that captures constraints and preferences. It could compile down to existing engines without a new DSL.

Here's an illustrative snippet for the "12 eggs" example:

```json
{
  "task": "buy_eggs",
  "quantity": 12,
  "constraints": {
    "max_spend": 5.00,
    "allowed_merchants": ["local_grocer", "organic_farm_co"],
    "geographic_limits": "within_10km",
    "delivery_sla": "under_2_hours",
    "substitutions_allowed": false,
    "dietary": ["organic", "free_range"]
  },
  "preferences": {
    "weights": {
      "cheapest": 0.6,
      "best_rated": 0.3,
      "fastest_delivery": 0.1
    },
    "brand_preferences": ["prefer_local"],
    "avoids": ["big_box_stores"]
  },
  "incentives": {
    "affiliate_bias": false,
    "sponsored_flags": ["disclose_if_present"]
  },
  "explainability": {
    "require_reason_codes": true,
    "top_alternatives": 3,
    "confidence_threshold": 0.8,
    "audit_trail_id": "optional_uuid"
  }
}
```

Constraints are hard rules: violate them, and the choice fails. Preferences are soft: weights for multi-objective optimization. Incentives flag biases like affiliates. Explainability hooks ensure traceability. Why this egg carton, not the others? It's auditable, which builds trust.

Keep it lightweight; this isn't exhaustive, just a starting point.

### Compiling to Existing Policy Engines

Why reinvent? Compile this schema to proven engines like OPA/Rego, Cedar, or Biscuit. They're battle-tested for policy-as-code.

For hard constraints: map to deny rules in OPA. If max_spend is exceeded, Rego could evaluate `deny if input.cost > policy.max_spend`. Simple boolean gates.

Soft preferences: these fit Cedar's authorization with attributes. Weights could inform a scoring function, then authorize based on thresholds. Biscuit's attenuation could chain preferences down sub-agents, diluting or enforcing them.

Conceptually, the schema acts as input data; the engine enforces. No new language, just leverage what's there. For eggs, constraints filter options; preferences rank the survivors.

This keeps things interoperable. Agents from different vendors consume the same schema, compile locally, and act consistently.

### Why OSS Reference Implementations Matter

OpenBotAuth is all OSS: specs, code, plugins. The goal isn't capture. It's ecosystem building. Neutral standards prevent silos, especially in auth and now selection.

The WordPress plugin shows this in action for publishers. It verifies bot authority and could extend to selection policies, letting sites expose choices that respect user prefs. Again, not pitching, just demonstrating how these layers integrate.

### Open Questions

This is thinking in public, so plenty of gaps.

Is a standardizable selection schema possible without becoming a monopoly tool? Who governs it?

Incentives and ads: how to mandate disclosure without stifling commerce? Flags are a start, but enforcement?

Telemetry and observability: where do trust boundaries end? Analytics for audit trails could help, but privacy tensions arise.

Builders, weigh in. Point me to papers, drafts, repos. What's missing in delegation? How should selection schemas evolve? Let's iterate.

---

*This started as an X thread about the gap between agent authority and agent selection. The egg example stuck because it's simple but captures the real problem: who decides how your agent decides?*

*Find me at [@hammadtariq](https://twitter.com/hammadtariq)*

