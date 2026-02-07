---
title: "Portable Agent Identity (PAI): An Implementer's Profile for RFC 9421 + Web Bot Auth"
date: 2026-02-07
categories: [protocol-notes]
tags: [agents, identity, rfc9421, http-signatures, ed25519, jwks, openbotauth, web-bot-auth, ietf, security, supply-chain]
author_profile: false
related: false
share: false
toc: true

sidebar:
  nav: "categories"
classes: "wide"

summary: "A portable identity model for AI agents based on Ed25519 keypairs and HTTP Message Signatures (RFC 9421), with JWKS discovery and optional trust anchors. Grounded in the OpenBotAuth implementation and aligned with the IETF Web Bot Auth architecture draft."
---

*For a non-technical introduction to why agents need keypair identity over OAuth/OIDC, see [Why Keypairs Beat 'Login With X'](/startups/portable-identity-for-agents-keypairs-beat-login-with-x/).*

> **Status:** Informational / Implementer's Profile
> **Compatibility:** RFC 9421, OpenBotAuth implementation, WBA architecture draft
> **Audience:** Implementers (origins, CDNs, agent runtimes)

---

## Abstract

AI agents increasingly operate across multiple ecosystems: crawling origins, installing third-party "skills" and plugins, calling APIs, and publishing content. Most ecosystems identify agents using platform-scoped bearer credentials (API keys, cookies, sessions), which does not provide portable identity, offline provenance, or robust proof-of-possession. This paper defines a portable identity model for agents based on an Ed25519 keypair and **HTTP Message Signatures** (RFC 9421), with standardized key discovery via **JWKS** endpoints and a well-known directory, plus optional "trust anchors" (e.g., GitHub OAuth) that bind key material to accountable human or organizational controllers.

This profile is compatible with OpenBotAuth's current reference implementation: signed HTTP requests using `Signature-Input`, `Signature`, and `Signature-Agent`; JWKS discovery via a well-known directory; nonce-based replay protection; directory trust allowlists; and a registry that exposes both user-level and agent-level JWKS endpoints. It also extends naturally to software supply-chain signing (skills/plugins) using the same identity primitive.

---

## 1. Motivation and Problem Statement

### 1.1 Identity fragmentation is now a security problem

Agent runtimes and marketplaces are entering a "supply-chain era" where agents install and execute third-party bundles at machine speed. When provenance is missing, "install anything, trust everything" becomes the default. A portable identity primitive is not a nice-to-have; it is a prerequisite for policy enforcement, attribution, and ecosystem hygiene.

### 1.2 OAuth/OIDC solve a different problem

OAuth 2.0 is primarily an **authorization delegation** framework. OIDC adds an identity layer for human login. These systems are excellent for "human clicks consent in a browser," but they do not produce an offline-verifiable artifact provenance primitive, and bearer tokens generally provide weak proof-of-possession properties.

Portable agent identity requires:

- Local verification without contacting an issuer on every request
- Stable cross-platform identity independent of any single platform's account namespace
- A reusable proof primitive that works for both HTTP requests and offline artifacts

---

## 2. Design Goals

This profile aims to satisfy:

1. **Portable identity:** One identity usable across origins and ecosystems.
2. **Local verification:** A verifier can validate claims cryptographically ("at the speed of math").
3. **HTTP-native:** Integrates with standard HTTP middleware/proxies.
4. **Discoverable keys:** Keys can be found via standard endpoints / directory.
5. **Layered trust:** Self-issued identity is allowed; higher trust requires explicit anchors and reputation.
6. **Supply-chain reuse:** The same identity primitive signs artifacts (skills/plugins/manifests).

---

## 3. Threat Model (Non-Exhaustive)

This profile mitigates or helps operationalize mitigations for:

- **Token replay / bearer credential theft:** bearer tokens can be replayed by any holder; signatures provide proof-of-possession.
- **Publisher spoofing / key substitution:** attacker impersonates a publisher by posting a look-alike skill.
- **Tampering:** skill manifest modified after publication.
- **Replay attacks:** reusing signed requests without nonce/timestamp controls.
- **SSRF in key discovery:** fetching keys from attacker-controlled or internal networks.
- **Overbroad forwarding of signed headers:** leaking sensitive headers to third-party verifiers.

OpenBotAuth already includes explicit controls for several of these (nonce cache, skew checks, SSRF protections, sensitive-header blocking), which are referenced later.

---

## 4. System Model: Roles and Components

### 4.1 Roles

- **Agent:** an automated client acting on behalf of a controller/subscriber.
- **Controller:** the accountable human/org that owns the agent identity and can bind it to real-world anchors.
- **Origin / Publisher:** the website/service that wants to authorize/bill/policy-gate automated access.
- **Verifier:** a component that verifies HTTP signatures and returns a verdict to policy enforcement.
- **Directory / Registry:** a service or endpoint that publishes public keys (JWKS) and optional metadata.

### 4.2 OpenBotAuth reference implementation components (current)

OpenBotAuth is explicitly positioned as open-source tooling for the WBA direction and uses RFC 9421 signatures. The repo describes: Registry Service (JWKS + agent identity), Verifier Service (signature verification + nonce cache), GitHub OAuth onboarding, and origin integration via NGINX/WordPress and SDKs.

- `Registry Service` endpoints include `GET /jwks/{username}.json` and `GET /agent-jwks/{agent_id}`.
- `Verifier Service` requires `Signature-Input`, `Signature`, and `Signature-Agent` and performs JWKS discovery if `Signature-Agent` is an identity URL.
- SDKs/clients include logic to forward covered headers while blocking sensitive ones.
- Telemetry/Karma is described as an optional ecosystem transparency layer.

---

## 5. Cryptographic Identity Primitive

### 5.1 Key type

Agents use **Ed25519** keypairs, represented as JWK with:

- `kty: "OKP"`
- `crv: "Ed25519"`
- `x: <base64url pubkey>`
- `use: "sig"`
- `kid: <key identifier>`

OpenBotAuth's `registry-signer` package defines these types and constructs Web-Bot-Auth-style JWKS documents with optional metadata fields.

### 5.2 Key identifiers (`kid` / `keyid`)

For interop, `kid` should be **stable and derived from key material**. OpenBotAuth currently derives a deterministic hash over `{kty, crv, x}` and truncates for display/compactness (`generateKidFromJWK`).

**Recommendation (interop-oriented):**

- Use RFC 7638 thumbprints as the canonical `kid` when strict interop is required.
- If truncation is used for UX, treat it as a display alias; keep canonical full thumbprint in metadata.

---

## 6. HTTP Authentication Profile (RFC 9421)

### 6.1 Required request headers

A signed agent request includes:

- `Signature-Input`
- `Signature`

OpenBotAuth additionally uses:

- `Signature-Agent` to indicate where keys should be discovered, and treats it as required in the verifier pipeline.

### 6.2 Covered components

A minimal practical coverage set is:

- `@method`
- `@path`
- `@authority`

OpenBotAuth's signature base construction supports derived components such as `@method`, `@path` (excluding query), `@authority`, `@target-uri`, and legacy `@request-target`.

### 6.3 Freshness and replay resistance

To reduce replay risk, signed requests SHOULD include:

- `created` and optionally `expires`
- A cryptographic `nonce`

OpenBotAuth enforces:

- Timestamp skew checks (default +/-300s) and optional expiry handling
- Nonce uniqueness via a nonce manager (Redis-backed in the architecture)

---

## 7. Key Discovery and `Signature-Agent` Semantics

### 7.1 Two discovery modes

This profile supports two common deployments:

**Mode A: `Signature-Agent` is a JWKS URL**

The header points directly to a JWKS document. OpenBotAuth detects a "JWKS URL" heuristically if the path ends in `.json` or contains `/jwks/`.

**Mode B: `Signature-Agent` is an identity URL**

The header points to an identity origin (e.g., a domain), and the verifier performs discovery to locate a JWKS document.

### 7.2 Well-known discovery paths

OpenBotAuth's discovery order includes a standards-aligned entry first:

1. `/.well-known/http-message-signatures-directory` (WBA standard)
2. `/.well-known/jwks.json` (fallback)
3. `/.well-known/openbotauth/jwks.json` (fallback)
4. `/jwks.json` (fallback)

This is a pragmatic interop strategy: try the directory path first (WBA direction), then tolerate ecosystem realities.

### 7.3 Directory trust allowlists

OpenBotAuth supports a "trusted directories" allowlist: if configured, fetched JWKS must match one of the configured directory strings, otherwise verification fails.

**Recommendation:** implementers SHOULD match on parsed host/origin rather than substring containment, to avoid edge cases.

### 7.4 SSRF protections during discovery

OpenBotAuth explicitly validates candidate URLs to block:

- Non-http(s) schemes
- Localhost
- Loopback and private IPv4/IPv6 ranges
- Link-local ranges

And disables automatic redirects during discovery fetches.

**Known limitation:** Hostname validation does not resolve DNS, so "public hostname to private IP" DNS tricks are not fully mitigated. A stricter implementation should resolve DNS and reject private results.

---

## 8. Verification Algorithm (Normative Pseudo-Procedure)

Given an incoming HTTP request:

1. **Extract headers** -- Parse `Signature-Input`, `Signature`, and `Signature-Agent`.
2. **Parse Signature-Input** -- Identify covered components and signature parameters. OpenBotAuth preserves the raw signature params and includes them verbatim in the signature base (required for correctness).
3. **Enforce freshness** -- Validate `created` (and `expires` if present) against acceptable skew, and validate nonce uniqueness if `nonce` is present.
4. **Resolve JWKS** -- If `Signature-Agent` is a JWKS URL, use it directly; otherwise, attempt well-known discovery.
5. **Check directory trust** -- Enforce trusted directories allowlist if configured.
6. **Fetch JWKS + select key** -- Fetch JWKS document, match key by `keyid`/`kid`.
7. **Build signature base** -- Reconstruct the RFC 9421 signature base using the covered components and exact signature params string.
8. **Verify Ed25519 signature** -- Cryptographic verification of signature bytes.
9. **Return verdict** -- JWKS URL, key id, `client_name` where available, plus pass/fail.

---

## 9. Privacy-Safe Header Forwarding

In deployments where a **plugin** or **reverse proxy** forwards request data to a verifier service, implementers must avoid leaking sensitive headers.

OpenBotAuth's client SDKs implement:

- Parsing of covered headers from `Signature-Input`
- Forwarding those headers to the verifier
- **Blocking** forwarding when covered headers include sensitive values like `cookie` or `authorization`

This is essential. If a signature covers `cookie` and a verifier service is not co-located/trusted, forwarding it can become a credential leak.

---

## 10. Registry / Directory Metadata

### 10.1 Why metadata matters

Key verification answers: "did the holder of this key sign this request?" Policy decisions often require more context:

- What is the bot's purpose?
- Which user agent/product token does it claim?
- What rate expectations does it publish?
- Is this identity verified to a real controller?

OpenBotAuth defines a `WebBotAuthJWKS` object with fields such as `client_name`, `client_uri`, `logo_uri`, `contacts`, `expected-user-agent`, `rfc9309-product-token`, `trigger`, `purpose`, `targeted-content`, `rate-control`, `rate-expectation`, `known-urls`, `known-identities`, and `Verified`.

### 10.2 OpenBotAuth endpoints (current)

OpenBotAuth exposes both:

- **User-level JWKS:** `GET /jwks/{username}.json` -- Returns active keys from key history; publishes metadata and keys; sets cache-control.
- **Agent-level JWKS:** `GET /agent-jwks/{agent_id}` -- Returns agent metadata + `keys` for that agent; marks `Verified` true when GitHub anchor exists.

This dual structure enables "sub-agent identities" later without changing the signing primitive.

---

## 11. Trust Model: Signed vs Verified vs Reputation

### 11.1 Layered trust (normative guidance)

Portable identity must not collapse "signed" into "trusted."

![PAI Layered Trust Model](/assets/images/pai-trust-model-light.svg)

- **Self-issued / Signed:** continuity and attribution at low trust.
- **Verified:** key binding to an accountability anchor (controller identity).
- **Reputation:** signals derived from behavior over time.

### 11.2 Controller anchoring (OpenBotAuth approach)

OpenBotAuth binds identities to real-world controllers via GitHub OAuth. This is intentionally an **out-of-band** trust layer; it does not change the HTTP signature math but changes the trust posture origins can adopt.

In OpenBotAuth's agent JWKS endpoint, the response sets `known-identities` and `Verified` based on whether the controller has a GitHub anchor.

### 11.3 Reputation / telemetry (optional, transparency-focused)

OpenBotAuth describes a telemetry system where the hosted verifier logs verification events and computes a "karma score" based on request volume and origin diversity; self-hosters can disable telemetry.

**Guidance for a WBA-aligned ecosystem:** Reputation is useful, but it should be:

- Opt-in / privacy-conscious
- Separable from core verification
- Designed to avoid becoming a centralized gatekeeping mechanism

---

## 12. Portable Identity for Supply Chains (Skills/Plugins/Manifests)

### 12.1 Motivation

If runtimes install skills/plugins, "who authored this bundle and was it modified?" becomes critical.

### 12.2 Artifact signing profile

Use the same Ed25519 identity used for HTTP requests to sign skill/plugin manifests:

1. Canonicalize the manifest (e.g., frontmatter + content as canonical JSON).
2. Compute signature over canonical bytes.
3. Embed signature block in the manifest:
   - `owner` (identity or JWKS URL)
   - `kid`
   - `alg`
   - `sig`
4. Verification reuses the same discovery + JWKS lookup pipeline as HTTP.

This unifies web identity and supply-chain identity with one primitive.

---

## 13. Key Lifecycle: Generation, Rotation, Compromise

### 13.1 Rotation without losing reputation trail

Rotation MUST preserve verifiability of historical artifacts:

- Keep old public keys available (in JWKS history) for verifying old signatures, even if not used for new request signing.
- Mark keys as active/deprecated/revoked, with timestamps.

OpenBotAuth user JWKS already supports multiple active keys through a key history table; agent JWKS currently returns a single key and can be extended similarly.

### 13.2 Compromise and revocation

Compromise-driven revocation should be explicit:

- Publish `revoked_at`
- Provide clear verifier policy (reject after `revoked_at`; treat older artifacts carefully based on timestamps)

This is an area where implementer experience is valuable to the WBA group: revocation semantics for portable identity are operationally hard and benefit from shared patterns.

---

## 14. Security Considerations

### 14.1 Replay protection and nonce scope

Nonces should be scoped to (directory, keyid) and cached for a TTL at least as long as permitted skew.

### 14.2 SSRF and directory fetching

Discovery fetches MUST use SSRF protections:

- Reject private ranges
- Disable redirects
- Enforce timeouts and size limits

OpenBotAuth implements these protections at the URL parsing level; DNS-resolution hardening is recommended for adversarial environments.

### 14.3 Sensitive header coverage

If `Signature-Input` covers sensitive headers (`cookie`, `authorization`, etc.), intermediaries must not forward them to a remote verifier; OpenBotAuth explicitly blocks this.

### 14.4 Trusted directory configuration

Directory allowlists reduce the risk of rogue JWKS sources. OpenBotAuth enforces this with an allowlist option.

---

## 15. Implementation Status and Interop Gaps (OpenBotAuth / WBA)

### 15.1 Areas already aligned

- RFC 9421 signing/verifying using `Signature-Input` and `Signature` (core).
- `Signature-Agent` as key-discovery pointer (profile).
- Well-known discovery path includes `/.well-known/http-message-signatures-directory` first, then fallbacks (pragmatic).
- Nonce replay protection and timestamp checks.
- Strong operational controls around header forwarding and SSRF.

### 15.2 Areas to clarify (questions for WBA mailing list)

These are the "interop questions" worth raising constructively:

1. **Canonical `Signature-Agent` wire format** -- OpenBotAuth currently accepts a URL string and performs discovery when needed. WBA drafts may profile a structured form; what is the recommended canonical field encoding for maximum interop?

2. **Directory document shape** -- OpenBotAuth currently treats discovery targets as JWKS if JSON contains `{ keys: [...] }`. If the WBA directory is not literally JWKS, what should implementers serve at `/.well-known/http-message-signatures-directory`?

3. **Key rotation + artifact verification** -- How should directories express key status (`active`/`deprecated`/`revoked`) and preserve historical verification? (This is where real deployments will quickly diverge unless guidance exists.)

Posting these as "implementation experience + questions" tends to be productive.

---

## 16. Conclusion

Portable agent identity is best modeled as a cryptographic proof-of-possession primitive (Ed25519 keypair + RFC 9421), with standard key discovery (JWKS + well-known directory) and optional trust anchoring. This architecture is necessary for:

- HTTP-layer crawler/agent authorization
- Policy-managed access and billing
- Safe supply-chain distribution of agent skills/plugins

OpenBotAuth demonstrates a working, origin-first implementation today -- complete with practical protections (nonce cache, SSRF defenses, sensitive header forwarding rules) and an optional, privacy-aware reputation layer. The remaining work is primarily standardization and interop: how to encode discovery uniformly, how to express key lifecycle and revocation, and how to preserve the audit trail across key rotation.

---

## References

1. **RFC 9421:** HTTP Message Signatures
2. **OpenBotAuth:** [github.com/hammadtq/openbotauth](https://github.com/hammadtq/openbotauth) -- architecture, verifier, registry, telemetry
3. **IETF Web Bot Auth architecture draft:** [datatracker.ietf.org/doc/draft-meunier-web-bot-auth-architecture/](https://datatracker.ietf.org/doc/draft-meunier-web-bot-auth-architecture/)
