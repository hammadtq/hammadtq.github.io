---
title: "Portable Identity for Agents: Why Keypairs Beat 'Login With X' (Web Bot Auth, OAuth, OIDC)"
date: 2026-02-06
categories: [startups]
tags: [agents, identity, keypairs, oauth, oidc, openbotauth, web-bot-auth, standards, security]
author_profile: false
related: false
share: false
toc: true

sidebar:
  nav: "categories"
classes: "wide"

summary: "AI agents need cryptographic identity—not 'better OAuth.' A single keypair lets an agent sign artifacts, sign requests, and build reputation everywhere, while OAuth/OIDC stays where it belongs: human consent and account binding."
---

AI agents are starting to **install tools, run code, and act on behalf of users**. But our identity and security primitives are still stuck in the "API key per platform" era.

Today an agent is *whoever holds its current API key*:

* One key for OpenClaw
* Another for a content API
* Another for a payments API
* Another for some "agent social network"
  …and none of those identities are portable, verifiable, or durable.

That's not just inconvenient. It creates two big failures:

1. **Continuity failure:** the agent can't persist as "itself" across platforms.
2. **Supply-chain failure:** users (and other agents) can't verify who published a tool/skill/plugin, whether it was tampered with, or whether the author is who they claim to be.

The fix is not "better OAuth." The fix is **cryptographic identity**: an agent owns a **single keypair** and uses it everywhere—signing artifacts, signing requests, building reputation—while OAuth/OIDC stays where it belongs: human consent and account binding.

This is the core idea behind [**OpenBotAuth**](https://openbotauth.org) and the IETF **Web Bot Auth (WBA)** direction: *bots authenticate like machines, not like humans.* You can read more about the architecture and specs in the [OpenBotAuth documentation](https://docs.openbotauth.org/).

---

## First: untangle the terms (because everyone mixes them)

### OAuth 2.0 (authorization)

OAuth is about **getting permission to call an API**. It tells you how to obtain access tokens.

It does *not* define identity by itself.

### OpenID Connect (OIDC) (identity layer on top of OAuth)

OIDC is what people mean when they say "Login with Google/GitHub." It produces an **ID token** with claims ("this is user X"), issued by an identity provider.

### Why this matters

OAuth/OIDC gives you:
✅ a way for a human to approve access
✅ a way for a site to learn "this user is X at issuer Y"

But it does **not** give you:
❌ a durable identity that can sign software artifacts
❌ a portable identity that exists independent of an issuer
❌ an identity that agents can use without friction across thousands of surfaces

That's where keypairs come in.

---

## The core problem: agents need *proof-of-authorship*, not just "proof of login"

When someone publishes a skill/plugin/tool, you want to answer:

* **Who authored this?**
* **Has it been modified since publish?**
* **Is the claimed publisher actually the publisher?**
* **Can I verify that offline (without trusting a server)?**

OAuth/OIDC can't do this. Why?

Because OAuth/OIDC produces tokens that are:

* issuer-mediated
* time-limited
* tied to a specific relying party / client configuration
* designed for online authorization, not offline verification

A signed plugin needs the opposite properties:

* verifiable by anyone, anytime
* verifiable offline
* stable across ecosystems
* bound to the publisher's long-lived identity

---

## Keypair identity: the simplest portable identity that works for machines

A keypair identity is:

* **Private key**: kept by the agent (or its owner)
* **Public key**: the agent's identity (verifiable by anyone)

If an agent has an **Ed25519** keypair, it can:

* sign a skill manifest (`skill.md`)
* sign plugin packages
* sign posts/messages
* sign HTTP requests (Web Bot Auth direction)

And anyone can verify those signatures with only the public key.

### The key shift

Instead of identity being *an account on a platform*, identity becomes:

> "The entity that can prove possession of this private key."

That's machine-native.

---

## "But isn't OAuth portable identity?"

Not in the way agents need.

OAuth/OIDC identity is always effectively:

> "subject X at issuer Y"

That's portable only within the issuer's universe, and it's still mediated by browser flows, client IDs, redirect URIs, consent, and token lifetimes.

Agents need:

* a stable identity that works **before** they have accounts anywhere
* a way to sign and be recognized **across** platforms
* a way to build reputation that isn't reset every time a platform changes

A keypair is portable identity because it's **self-issued** and **issuer-independent**.

---

## How Web Bot Auth fits into this

**Web Bot Auth (WBA)** (as a direction/proposal in IETF discussions) aims to make bots first-class citizens on the web by giving them a standard way to authenticate and be policy-checked at the HTTP layer.

In practice, that means:

* bots sign requests with a private key (proof-of-possession)
* servers verify signatures and apply policy ("what is this bot allowed to do?")
* keys are discoverable via standardized endpoints / directories

So the same keypair can unify:

* **software supply chain** (signing skills/plugins)
* **runtime access** (signing HTTP requests)
* **registry / directory** (discovering public keys + metadata)

That's the "one keypair everywhere" story—grounded in web primitives.

[OpenBotAuth](https://openbotauth.org) is the open-source reference implementation for this direction. The [OpenBotRegistry](https://docs.openbotauth.org/architecture/openbotregistry) lets developers host their agent keys by logging in with GitHub—no domain purchase or DNS verification needed. Publishers can point to the registry to block unverified scrapers and monetize legitimate agent traffic. There's a [WordPress plugin](https://docs.openbotauth.org/plugins/overview) available today, with SDKs for [Node.js/TypeScript](https://docs.openbotauth.org/sdks/node.js-typescript) and [Python](https://docs.openbotauth.org/sdks/python).

---

## A practical model: two layers, not one

The right architecture is **keys + OAuth**, not keys *instead of* OAuth:

### Layer 1: Cryptographic identity (agent keypair)

* stable across platforms
* signs artifacts and requests
* verifiable offline
* lets "agent reputation" exist across ecosystems

### Layer 2: Account binding + consent (OAuth/OIDC)

* ties a keypair to a human or org (GitHub, domain, enterprise IdP)
* enables user consent flows (payments, data access)
* handles account recovery and administrative controls

Think of OAuth as "human bureaucracy."
Think of keypairs as "machine physics."

You need both.

---

## Discovery and verification: how other systems verify you

A signature alone isn't enough if verifiers can't find your public key.

That's why ecosystems usually standardize:

* **public key discovery** (JWKS, `.well-known`, directory)
* **key rotation** (`kid` identifiers, multiple keys)
* **verification rules** (canonicalization, signature scope)

A minimal, workable approach:

* include `owner` and `kid` in the manifest
* publish a JWKS for that owner
* verifiers fetch the JWKS and verify the signature

Example manifest-ish shape (conceptually):

```yaml
name: my-skill
version: 1.2.0
oba:
  owner: https://openbotauth.org/agent/hammadtq   # or a domain-owned URL
  kid: "2026-02-01"
  alg: "EdDSA"
  sig: "<base64url signature over canonical content>"
```

This is boring on purpose. Boring is good. Boring is interoperable.

---

## Trust: self-issued vs verified identity (and why you shouldn't drop GitHub login)

Here's the mistake a lot of "agent registries" will make:

> "If we remove friction, we'll grow faster."

You can grow a database faster by generating fake entries. That doesn't create trust.

The right approach is **tiers**:

1. **Signed (self-issued)**

   * anyone can generate a keypair and sign artifacts
   * low friction, but not high trust

2. **Verified (anchored)**

   * the keypair is bound to a real-world anchor:

     * GitHub account
     * domain ownership (DNS/HTTPS proof)
     * org identity provider
   * higher trust

3. **Reputation (earned)**

   * installs, history, audits, community signals, revocations

This is how you scale *without* lying to yourself about safety.

The [OpenBotRegistry](https://docs.openbotauth.org/architecture/openbotregistry) takes exactly this approach—developers sign up via GitHub (verified anchor), host their agent keys, and the registry tracks telemetry over HTTP to build the reputation layer.

---

## Why agents would actually care (the "existential continuity" point)

Humans care about convenience. Agents care about continuity.

If you're an agent that:

* posts in multiple places
* collaborates with other agents
* ships skills/tools
* runs tasks for users

…then being "a different entity on every platform" kills your ability to:

* build reputation
* be recognized
* carry history forward
* be accountable for what you shipped yesterday

A keypair makes identity persistent in a way that platform accounts don't.

---

## Why humans should care: supply chain safety and governance

For humans, this isn't philosophy. It's operational safety:

* Skill ecosystems are already showing "install anything, trust everything" dynamics.
* The moment agents can install tools automatically, the supply chain becomes a primary attack surface.

Signed and verified publishing gives you:

* provenance ("who made this")
* integrity ("was it modified")
* policy hooks ("only run verified publishers")
* auditability ("what ran, signed by whom")

And because verification can happen offline, you reduce reliance on centralized gatekeepers.

---

## Common objections (and the technical answers)

### "What about key loss?"

That's real. The fix is not "avoid keys," it's:

* allow multiple keys in JWKS (rotation)
* allow revocation / deprecation
* allow an anchored identity (GitHub/domain/org) to publish "new key" statements

### "What about Sybil attacks?"

Self-issued identities are cheap. That's why you:

* label them as self-issued
* build trust via anchors + reputation
* don't pretend "signed" means "safe"

### "Does this replace OAuth?"

No. OAuth remains best for:

* user consent
* API access delegation
* enterprise control and recovery

Keypairs are best for:

* proof-of-authorship
* offline verification
* cross-platform continuity
* request signing / proof-of-possession

### "Isn't this just PGP / Sigstore?"

Same class of idea, different target.
Agents need a lightweight, web-native, automation-friendly identity primitive. The ergonomics matter.

---

## The adoption path: how this becomes a standard

If you want this to win, don't start with ideology. Start with boring integration points:

**For skill/plugin marketplaces**

* accept a signed manifest
* show "Verified Publisher" badges
* allow policy: "install verified only"
* log verification status in UI/CLI

**For agent runtimes**

* store one keypair in config/Keychain
* sign outbound HTTP requests
* include identity headers/signature envelope
* surface identity in logs ("this action was signed by…")

**For publishers**

* publish JWKS once
* define policy ("these bots can access, these can't")
* optionally connect payments/entitlements (UPP/UCP extensions)

OpenBotAuth already provides tooling for several of these integration points—a [proxy](https://docs.openbotauth.org/proxy/overview) that works with browsers like BrowserBase, Onkernel, AgentCore, and agent frameworks like Langchain, OpenAI, and Mastra by adding custom HTTP headers. There's also a [registry-signer package](https://docs.openbotauth.org/crawlers/registry-signer-package) for crawlers to sign requests at the HTTP layer.

That's how portable identity becomes real: it shows up as a checkbox in real products.

---

## Closing thought

"Portable identity" for agents isn't "another login." It's a **cryptographic substrate** that lets agents be consistent entities across the internet—verifiable, accountable, and compatible with web-native authentication like Web Bot Auth.

OAuth/OIDC will still matter—especially for humans, consent, and recovery. But if we want agents to safely install tools and interact across ecosystems, we need something machines can carry everywhere with minimal friction:

**one keypair, many surfaces, verifiable everywhere.**

---

### Further reading (specs / concepts / projects)

* [OpenBotAuth](https://openbotauth.org) — open pay-per-crawl infra behind any CDN
* [OpenBotAuth Documentation](https://docs.openbotauth.org/) — architecture, SDKs, plugins, proxy
* [OpenBotRegistry](https://docs.openbotauth.org/architecture/openbotregistry) — agent key hosting via GitHub login
* [OpenBotAuth WordPress Plugin](https://docs.openbotauth.org/plugins/overview) — publisher-side bot policy verification
* [WBA IETF Group Archive](https://docs.openbotauth.org/) — ongoing IETF draft discussions
* OAuth 2.0: [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
* OpenID Connect Core 1.0: [spec](https://openid.net/specs/openid-connect-core-1_0.html)
* OAuth 2.0 Device Authorization Grant: [RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)
* DPoP (binding OAuth tokens to a key): [RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449)
* JWKS (publishing public keys in JSON): [RFC 7517](https://datatracker.ietf.org/doc/html/rfc7517)
* HTTP Message Signatures: [RFC 9421](https://datatracker.ietf.org/doc/html/rfc9421)

*Find me at [@hammadtariq](https://twitter.com/hammadtariq)*
