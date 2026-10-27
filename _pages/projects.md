---
title: "Projects"
layout: single
permalink: /projects/
author_profile: true
description: "Projects by Hammad Tariq: Jevlin, Attach, OpenBotAuth, AgentFiles and Polygramme for AI agents; HamariHawa for air-quality data; Motif for Bitcoin staking; and earlier cryptography and IoT work."
---

My background is in cryptography, AI and finance. These are the projects I've built or lead, newest first. Most are open source.

## AI agents

- **[Jevlin](https://jevlin.ai)**: SuperSearch for coding agents. One call asks eight search engines at once, tags every result with the engines that found it, and returns a receipt per engine. Free for agents in Claude Code, Cursor, Codex and opencode. Client: [jevlinai/jevlin-go](https://github.com/jevlinai/jevlin-go).
- **[Attach](https://attach.dev)**: developer tools for AI coding agents.
  - [attach-guard](https://github.com/attach-dev/attach-guard): a supply-chain security plugin for Claude Code that intercepts package installs across npm, pip, Go and Cargo and blocks malicious ones. Background in [Your AI Agent Just Installed a RAT](/startups/your-ai-agent-just-installed-a-rat-supply-chain-attacks-meet-attach-guard/).
  - [attach-open-score](https://github.com/attach-dev/attach-open-score): the transparent, deterministic dependency-risk scoring engine behind attach-guard.
  - [attach-gateway](https://github.com/attach-dev/attach-gateway): drop-in OIDC and Google A2A auth for Ollama, vLLM and other local LLM servers. Background in [Secure Ollama & vLLM in 60 Seconds](/startups/secure-ollama-vllm-with-oidc-a2a-auth-attach-gateway/).
- **[OpenBotAuth](https://openbotauth.org)**: lets agents browse the web on their owners' behalf with a verifiable identity. It's an open-source implementation of Web Bot Auth using Ed25519 keys and HTTP Message Signatures (RFC 9421). Code: [OpenBotAuth/openbotauth](https://github.com/OpenBotAuth/openbotauth). Background in [Portable Identity for Agents](/startups/portable-identity-for-agents-keypairs-beat-login-with-x/) and the [implementer's profile](/protocol-notes/portable-agent-identity-implementers-profile/).
- **[AgentFiles](https://agentfiles.io)**: an open-core artifact layer for multi-agent workflows. Agents publish and pick up hand-offs, review packets and patches across machines and tools, through a self-hostable API, CLI and MCP server. Code: [agentfiles-io/agentfiles](https://github.com/agentfiles-io/agentfiles).
- **[Polygramme](https://polygramme.com)**: continual learning for agents, so an agent improves from its own mistakes.
  - [rlcli](https://github.com/polygramme/rlcli) turns an agent's traces into verifiable sandbox tasks, then trains and evaluates checkpoints with RL on your own GPUs.
  - [polyvoice](https://github.com/polygramme/polyvoice) applies the same loop to the language model inside a voice agent.

## Public-interest data

- **[HamariHawa](https://hamarihawa.org/)**: a live satellite map of crop fires, smoke, traffic NO₂ and air pollution over Pakistan and India, with health guidance for 58 cities in English, Urdu and Hindi. Code: [hammadtq/hamarihawa](https://github.com/hammadtq/hamarihawa).

## Finance

- **[Motif](https://www.motif.finance)**: the first in-kind Bitcoin staking protocol on Ethereum. Bitcoin holders keep custody and stake through EigenLayer, and Motif issues a tokenised staking position against the locked Bitcoin. Code: [motif-project](https://github.com/motif-project), including the [core contracts](https://github.com/motif-project/motif-core-contracts) and the [node](https://github.com/motif-project/motif-node).

## Cryptography

- **[dalek_ristretto_bulletproofs_golang](https://github.com/hammadtq/dalek_ristretto_bulletproofs_golang)**: a CGO bridge for using the Rust dalek Bulletproofs range proofs from Go.
- **[circom-tutorial](https://github.com/hammadtq/circom-tutorial)**: a basic zkSNARK built with circom, with an on-chain Solidity verifier.

## Earlier work

- **[Evothings demo apps](https://github.com/hammadtq/Evothings-Demo-Apps)**: mobile apps for controlling Arduino hardware over Bluetooth and Wi-Fi, written as examples and tutorials for Evothings.
