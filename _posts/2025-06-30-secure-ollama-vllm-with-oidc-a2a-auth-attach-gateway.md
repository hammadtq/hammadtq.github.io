---
title: "Secure Ollama & vLLM in 60 Seconds: OIDC + A2A Auth with Attach Gateway"
subtitle: "I Left My GPU Unlocked for Five Minutes and Somebody Curled It"
date: 2025-06-30
categories: [startups]
tags: [startups]

# Turn off any right‐side elements you don’t want
author_profile: false
related: false
share: false
toc: false

sidebar:
  nav: "categories"
classes: "wide"

summary: "Attach Gateway secures Ollama and vLLM in one pip install—OIDC + Google A2A JWT auth, session headers, and Weaviate logging for audit-grade memory."
---

> “Auth is a TODO, feel free to PR.”
> — every GitHub thread on local LLM stacks, ever

## Two weeks ago I thought I was done.
Ollama was humming, vLLM was cranking out tokens, the office smelled of freshly-minted embeddings. Then a junior dev innocently pasted curl http://10.0.0.42:8000/completions into Slack and—boom—my entire RTX box lit up like a cheap arcade machine.
That’s when I learned the hard way that “secure by default” is still on vacation.

## The Endless Scroll of “Is Auth Supported?”
Don’t believe me? Here’s your bedtime reading:

	- vLLM issue #7547 — “What’s the recommended way to implement API keys?”  ￼
	- Ollama issue #1053 — “Requesting support for basic auth or API key authentication.”  ￼

Each thread ends with a variation of: “Just put Nginx in front of it, mate.”

**Great, another proxy to babysit.**

Meanwhile, Google Is Busy Standardising Agent-to-Agent Auth

Google Cloud quietly dropped the A2A protocol, and if you haven’t read the spec, picture OAuth for AI agents that want to invoice each other. Enterprises love it, and you can bet Big G will expect every endpoint in sight to verify an A2A JWT.  ￼

Local stack? Meet enterprise expectation. Spoiler: they don’t handshake.

---

## Attach Gateway — My Two-Line Fix for a Year-Old Problem

So I did what any sleep-deprived founder with a half-finished coffee would do: wrote a single-process Gofer that just handles the boring stuff.

```bash
pip install attach-dev
attach-gateway --upstream http://localhost:11434   # or your vLLM port
```

Sixty seconds later:

	- Real auth — OIDC and DID tokens verified; X-Attach-User + X-Attach-Session stamped on every request.
	- A2A-ready — /a2a/tasks/send endpoint speaks Google’s dialect natively.
	- Memory — prompts + completions mirrored into Weaviate because “who said what?” always becomes a legal question later.
	- Zero config — no Caddy, no hand-rolled nginx.conf, no Post-It on your monitor saying “remember to rotate keys”.

I called it Attach Gateway because it literally attaches to anything that talks HTTP and spits out JSON tokens.

---

## Why I Care (and Why You Should)
	- Multi-tenant chaos turns into neat tenant isolation. No more shared API keys floating in Notion pages.
	- Audit trails for regulated customers. If they can’t grep it, they won’t buy it.
	- Future-proof against A2A. When Google Cloud Support pings your endpoint, you’ll answer with a handshake, not a 401.

---

## The Road Ahead (a.k.a Features I Want Before Somebody Else PRs Them)
	- RBAC driven by Cedar or OPA because YAML is love, YAML is life.
	- Built-in rate limiting so my GPU fans don’t file a noise complaint.
	- Helm chart for the Kubernetes aficionados who deploy YAML for breakfast.

---

## Call to Action

If you’re tired of playing bouncer for your own model server, grab Attach Gateway, give it a spin, and tell me what breaks. The repo’s here: [github.com/attach-dev/attach-gateway](https://github.com/attach-dev/attach-gateway). PRs, issues, unsolicited memes — all welcome.

Because life is too short to copy-paste the same JWT proxy one more time.

[Article co-authored by GPT-o3]