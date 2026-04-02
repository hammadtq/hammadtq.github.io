---
title: "Your AI Agent Just Installed a RAT"
subtitle: "Two Supply Chain Attacks in One Week. Here's What Stops the Third."
date: 2026-04-01
categories: [startups]
tags: [ai, agents, security, supply-chain, attach, attach-guard, claude-code]
author_profile: false
related: false
share: false
toc: true

sidebar:
  nav: "categories"
classes: "wide"

summary: "axios and litellm were both compromised within a week — one by North Korean state actors, the other by stolen CI credentials. AI coding agents would have installed both without blinking. attach-guard is the open-source hook that blocks malicious packages before they touch your machine."
---

Last Monday I [quote-tweeted](https://x.com/hammadtariq/status/2038828755632918929?s=20) Feross's alert about the axios compromise and wrote:

> "Claude code should come with a dedicated dependency risk checker. Can't rely on socket-dev mcp, automatic enforcement is required."

Two days later I shipped [attach-guard](https://attach.dev/attach-guard).

This post is the full story: what happened to axios and litellm, why AI coding agents make supply chain attacks dramatically worse, and how a single Claude Code hook would have stopped both.

---

## One Week, Two Megapackages, Zero Human Reviewers

### axios — March 31, 2026

axios is one of npm's most depended-upon packages. Over 100 million weekly downloads. On March 31st, somebody hijacked the primary maintainer account (`jasonsaayman`), changed the associated email to a Proton address, and published two poisoned versions: **`axios@1.14.1`** and **`axios@0.30.4`**.

The only change in both: a new dependency — `plain-crypto-js@4.2.1`. A package that did not exist the day before.

That package ran a `postinstall` hook executing an obfuscated 4,209-byte JavaScript dropper. The payload: **WAVESHAPER.V2** — a cross-platform RAT with command execution, system exfiltration, and persistence capabilities across Windows, macOS, and Linux.

Google/Mandiant attributed it to **UNC1069**, a financially motivated North Korea-nexus threat actor active since at least 2018.

Socket.dev's scanner caught `plain-crypto-js` within six minutes of publication. The malicious versions were live for roughly two to three hours.

Two hours is more than enough when agents install packages autonomously.

### litellm — March 24, 2026

One week earlier: litellm, the LLM proxy that half the AI developer ecosystem depends on.

A threat actor known as **TeamPCP** stole PyPI publishing credentials via a compromised Trivy GitHub Action in litellm's CI/CD pipeline, then uploaded **`litellm==1.82.7`** and **`litellm==1.82.8`** directly to PyPI — bypassing the normal release process entirely.

The malicious wheel contained `litellm_init.pth`. If you're not familiar with Python's `.pth` trick: those files execute automatically every time the Python interpreter starts. No import needed. Just existing in `site-packages/` is enough.

The double-base64-encoded payload:

- **Stage 1**: Harvested environment variables, API keys, SSH keys, Git credentials, AWS/GCP/Azure/K8s configs, Docker credentials, shell history, crypto wallets, SSL private keys, CI/CD secrets, and database credentials.
- **Stage 2**: Encrypted everything with AES-256-CBC + a hardcoded 4096-bit RSA public key, then exfiltrated via POST to `models.litellm.cloud` — an attacker-controlled lookalike domain, not the real `litellm.ai`.

Also live for roughly three hours.

### The pattern

Both attacks targeted maintainer or CI credentials. Both were live for hours. Both hit packages that AI developers install constantly. And both would have been caught by the same two signals: **a suddenly cratered supply chain score** and **a version younger than 48 hours**.

---

## AI Agents Made This Worse

Here's the part that keeps me up at night.

Claude Code, Cursor, Copilot — they run `npm install` and `pip install` autonomously, dozens of times per session. No human squinting at the dependency diff. No one to ask "wait, since when does axios need `plain-crypto-js`?"

The agent sees a task, decides it needs a package, installs it, and moves on. The entire compromise lifecycle — from `npm install` to RAT on your machine — happens in the time it takes you to sip your coffee.

**"But I have Socket.dev's MCP server."**

Good. MCP servers provide advisory context. They inform. They do not enforce. The agent can acknowledge the warning, weigh it against the task, and install anyway. That's by design — MCP is context, not a guardrail.

**"What about a skill?"**

Skills are instructions the agent follows when invoked. They guide behavior, but they cannot block actions. An agent can skip a skill. It cannot skip a hook.

The gap was obvious: no open-source, local-first guardrail that sits directly in front of the install command and says **no**.

---

## attach-guard: A Hook, Not a Suggestion

[attach-guard](https://attach.dev/attach-guard) is a Claude Code **PreToolUse hook** that intercepts package installation commands and evaluates them against policy **before execution**.

The distinction matters:

| Mechanism | What it does | Can Claude bypass it? |
|---|---|---|
| **MCP server** | Provides advisory context | Yes — it's informational |
| **Skill** | Instructions Claude follows when invoked | Yes — can be skipped |
| **Hook** | Intercepts tool calls deterministically | **No** — runs before execution |

A security guardrail must be a hook because enforcement requires interception at the tool-call boundary, before the command ever runs.

### How it works

When Claude calls the Bash tool with something like `npm install axios`:

1. Claude Code fires the PreToolUse hook before execution
2. The hook pipes the tool input JSON to `attach-guard hook` via stdin
3. attach-guard parses the command, queries Socket.dev for risk scores
4. Returns a decision: **allow**, **ask** (with explanation), or **deny** (blocked)
5. On internal errors, exits with code 2 to **fail closed**

### Smart version replacement

Most security tools just say "no." attach-guard says "no, but here's a safe alternative."

When a risky version is blocked, attach-guard finds the newest version that passes policy and offers it as a replacement:

```
> npm install axios

attach-guard evaluates:
  axios@1.14.1  →  DENY (supply chain score 40, below threshold 50 — compromised)
  axios@1.14.0  →  ALLOW (supply chain score 71, passes all policy checks)

Result: ASK + rewritten command
  "npm install axios@1.14.0"
```

Claude sees the safe alternative and proceeds immediately. Your flow doesn't stop — it gets redirected to a safe path.

| Scenario | Example | Decision | What happens |
|---|---|---|---|
| Package is safe | `npm install axios@1.14.0` | **Allow** | Install proceeds normally |
| Pinned to compromised version | `npm install axios@1.14.1` | **Deny** | Blocked — supply chain score 40 |
| Unpinned, latest is risky | `npm install axios` | **Ask + rewrite** | Safe alternative offered: `axios@1.14.0` |
| All versions fail | malware-only package | **Deny** | Blocked with clear explanation |

Your flow only fully stops when there is genuinely no safe version to offer.

### Multi-ecosystem

attach-guard supports npm and pnpm today, with **pip, go get, and cargo add** shipping now — covering all four ecosystems where these attacks happened. The litellm attack was a PyPI compromise; the axios attack was npm. Same guardrail, both covered.

---

## What Would Have Happened

Let's rewind the clock.

### axios — with attach-guard installed

Your agent decides it needs axios and runs `npm install axios`.

1. attach-guard intercepts the command before execution
2. Resolves latest version: `axios@1.14.1`
3. Queries Socket.dev: **supply chain score 40** — well below the deny threshold of 50
4. **DENY**. The install never runs.
5. attach-guard walks back through recent versions, finds `axios@1.14.0` with a score of 71
6. Returns an **ASK** with a rewritten command: `npm install axios@1.14.0`
7. Claude proceeds with the safe version. WAVESHAPER.V2 never touches your machine.

### litellm — with attach-guard installed

Your agent runs `pip install litellm`.

1. attach-guard intercepts the command
2. Resolves latest: `litellm==1.82.8`
3. Queries Socket.dev: flagged as known malware, supply chain score in the floor
4. **DENY**. The `.pth` payload never lands in your `site-packages/`
5. Falls back to `litellm==1.82.6` — the last clean version
6. Your API keys, SSH keys, and cloud credentials stay where they belong

Both attacks would also have been caught by the **48-hour minimum age policy** — both malicious versions were brand new, published hours before detection. attach-guard denies versions younger than 48 hours by default.

Every decision gets logged to a local JSONL audit trail — who, what, when, why, and which policy rule fired. When your security team asks "were we affected?", you have the receipts.

---

## Two Commands, Done

```bash
claude plugin marketplace add attach-dev/attach-guard
claude plugin install attach-guard@attach-dev
```

That's it. The hook, config, and skill are all registered automatically. You'll need a [Socket.dev](https://socket.dev) API token (free tier available) — Claude Code will prompt you during setup.

Once running:
- **Automatic enforcement** — `npm install`, `pnpm add`, `pip install`, `go get`, and `cargo add` commands are intercepted and checked
- **`/explain <package>`** — look up any package's risk score, alerts, and version history from inside Claude Code
- **Configurable policy** — tune score thresholds, allowlists, denylists, and age requirements in `~/.attach-guard/config.yaml`

Full docs and source: [attach.dev/attach-guard](https://attach.dev/attach-guard)

---

Because life is too short to let your AI agent install a North Korean RAT while you're getting coffee.

Find me at [@hammadtariq](https://twitter.com/hammadtariq).

[Article co-authored by Claude]
