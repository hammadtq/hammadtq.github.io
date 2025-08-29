---
title: "From ‘Trust Us’ to ‘Prove It’: A Confidential Lane for AI Inference"
date: 2025-08-29
categories: [startups]
tags: [privacy, verifiable-compute, inference, security, governance]

# Turn off any right‐side elements you don’t want
author_profile: false
related: false
share: false
toc: true

sidebar:
  nav: "categories"
classes: "wide"

summary: "A founder’s take on moving AI inference from promises to portable proofs—without boiling the ocean."
---

Most AI inference today runs on policy and promises: “no training on your data,” “short retention,” and so on. That’s fine for low‑risk use. But as prompts start touching crown‑jewel assets—customer data, legal drafts, proprietary R&D—security teams increasingly want something stronger than policy: **proof**.

This post sketches a direction I’m exploring. It’s not a product announcement; it’s a map of where the industry can go.

## Why ‘confidential’ needs to become ‘verifiable’

Teams keep circling three practical problems:

1. **Runtime opacity.** You rarely know what exact runtime and model binary processed your prompt—or who could read it along the way.
2. **Linkability.** Even if content is encrypted, metadata can still tie requests back to specific users or accounts.
3. **Auditability.** Security wants an immutable, vendor‑neutral record that this model handled that input under these policies—not a slide deck.

The building blocks to address this exist. The work is packaging them into a portable lane any team can adopt across vendors.

## A minimal ‘confidential lane’

Think of a narrow, high‑assurance path your sensitive requests can take:

1) **Attested execution.**
Use hardware‑based isolation with remote attestation so clients can verify the measured runtime and model before any plaintext is handled. Only when policy checks pass does a secure session open end‑to‑end with the isolated runtime. See enclave attestation and verifier posture in major clouds (e.g., Google Cloud Confidential Space: https://cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview).

2) **Unlinkability by default.**
Send requests through privacy‑preserving relays or one‑time, unlinkable access grants so serving endpoints can’t tie calls back to an identity. Providers see quotas and ciphertext—not who you are. See Oblivious HTTP for unlinkable request relays (RFC 9458: https://www.rfc-editor.org/info/rfc9458) and Vitalik’s note on one‑time access tokens (https://x.com/VitalikButerin/status/1960311135686529304).

3) **Verifiable call receipts.**
Each call returns a compact receipt binding “what ran” to “what was processed” and “under which policy,” signed by the attested runtime. Receipts are easy to verify and easy to store for later audit. No screenshots, no trust fall.

We can't guarantee in this implementation but it’s a practical posture: **only the isolated runtime and the client see plaintext; the request is unlinkable; and you keep a portable, verifiable record.**

## Why now

- **Hardware is ready enough.** Confidential execution on modern accelerators has matured; the overhead is acceptable for high‑value traffic. NVIDIA H100 confidential computing: https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/ · Azure GA for H100 confidential VMs: https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/general-availability-azure-confidential-vms-with-nvidia-h100-tensor-core-gpus/4242644 · Performance considerations (research): https://arxiv.org/html/2409.03992v2
- **Protocols matured.** Privacy‑preserving relay patterns make unlinkability feasible without contorting your stack (RFC 9458 OHTTP: https://www.rfc-editor.org/info/rfc9458).
- **Buyers are primed.** Regulated teams already pay for HSMs, clean rooms, and audit trails; they’ll adopt a “secure lane” if it’s simple and portable.

## What this is not

- A guarantee that “no system anywhere ever cached anything.” You can’t disprove what you don’t control. You can prove your exact code path didn’t write plaintext, and that only an attested runtime could decrypt the session.
- A bet that every token needs heavy cryptography. Use stronger guarantees where they matter most; keep the lane narrow and valuable.

## Open questions I’m exploring

- **Performance envelopes.** Where does the secure lane clearly pay for itself?
- **Side‑channel posture.** What developers need to know about timing and I/O patterns.
- **Policy UX.** Binding eligibility (e.g., jurisdiction or role) using selective‑disclosure credentials—without oversharing.
- **Interoperability.** A neutral receipt format that works across clouds and models so auditors don’t relearn per vendor.

## Founder note

This line-of-thinking isn’t about distrusting providers; it’s about giving security and compliance teams a **portable proof** that survives org charts and roadmap shifts. My bias here: The steady‑state for sensitive inference is **trust‑minimized by design**—and simple enough that engineers actually turn it on.

If you’re piloting this class of guarantees and want to compare notes, reach out.

_[Written with GPT‑5 Thinking]_ 

---

### References

- Vitalik on unlinkable, one‑time access tokens (X/Twitter): https://x.com/VitalikButerin/status/1960311135686529304
- Oblivious HTTP (OHTTP), RFC 9458: https://www.rfc-editor.org/info/rfc9458
- NVIDIA: Confidential computing on H100 GPUs: https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/
- Azure GA: Confidential VMs with NVIDIA H100: https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/general-availability-azure-confidential-vms-with-nvidia-h100-tensor-core-gpus/4242644
- Research: Performance considerations for GPU confidential computing: https://arxiv.org/html/2409.03992v2
- Google Cloud Confidential Space overview (attestation): https://cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview
- OpenRouter: Zero Data Retention and prompt caching docs: https://openrouter.ai/docs/features/zdr


