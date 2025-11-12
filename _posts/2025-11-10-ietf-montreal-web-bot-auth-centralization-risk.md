---
title: "Web Bot Auth After Montreal: The Power Shift We Shouldn’t Ignore"
date: 2025-11-10
categories: [startups]
tags: [ietf, identity, bots, cloudflare, http, rfc9421, decentralization]
author_profile: false
related: false
share: false
toc: true

sidebar:
  nav: "categories"
classes: "wide"

summary: "The IETF’s web bot authentication push is meant to make AI crawlers verifiable, but it risks handing control of identity to large CDNs. Here’s what really happened in Montreal, why people are uneasy, and how we can keep the web open."
---

I spent the last few days sifting through the recordings of IETF 124 in Montreal. I was particularly interested in "web bot auth" related sessions. What started as a technical discussion about making web crawlers more accountable turned into battle over who gets to control identity on the open web.

The basic idea seems reasonable enough: instead of websites trying to guess which bots are legitimate based on IP addresses or user agents (both easily spoofed), let the bots cryptographically sign their requests. Website sees the signature, checks it against a public key, and knows exactly who's knocking.

In simpler terms: scrapers want to scrape and sites want to control access, but instead of an endless arms race, how can we create structure around this push-and-pull?

But here's the thing—once you can definitively identify every bot, you can also control every bot. And that's where this gets interesting.

### The Demo That Worked Too Well

The technical demo was actually pretty elegant. A bot makes an HTTP request, signs it using RFC 9421 (HTTP Message Signatures), and includes a header pointing to where its public key lives. The receiving server verifies the signature and decides what to do. There are no complex OAuth dances, no bearer tokens floating around—just cryptographic proof that "this request definitely came from that specific agent."

![Web Bot Auth Architecture](/assets/images/web-bot-auth-flow.png)

The architecture cleanly separates identity verification from policy decisions. The verifier library fetches keys from the agent's own directory, while the policy engine makes independent decisions about access, rate limiting, or billing.

It replaces the current mess where sites maintain IP allowlists for "good" crawlers like Googlebot, which breaks constantly and is trivial to circumvent.

The demo worked flawlessly. That's exactly the problem.

---

### Why People Are Getting Nervous

The pushback isn't about the crypto or the technical implementation—it's about what happens next.

**First, there's the centralization trap.** The IETF drafts have agents host their own verification keys at origin endpoints. The risk isn't in key hosting—it's in verification. If most sites end up relying on a few CDNs to handle signature verification "for convenience," we've recreated the certificate authority problem through deployment patterns, not protocol design. Whoever controls the most-used verification infrastructure effectively decides which crawlers get widespread acceptance.

**Second, money changes everything.** I watched presentations from companies like TollBit and Skyfire talking about their "No Free Crawls" programs. Once you can cryptographically prove which bot made which request, billing becomes trivial. The rate limiting gets easy and the line between "identity verification" and "paywall infrastructure" starts to blur pretty quickly.

**Third, some vendors are pitching managed key custody "for convenience."** The spec doesn't require this—agents are supposed to control their own signing keys—but I keep hearing it in sales pitches. If I'm running a crawler, I want to control my own keys. When something goes wrong—and it will—I want clear accountability. Managed custody just makes everything murkier.

**Finally, there's the replay risk.** RFC 9421 gives you timestamps, nonces, and path binding to prevent cross-context replays, but implementations need to use them properly. HTTP signatures survive proxies by design, which is good, but sloppy signature component choices could enable replays in unintended contexts. This is more about implementation hygiene than a fundamental flaw.

---

### Don't Get Me Wrong—This Isn't All Bad

RFC 9421 itself is actually solid engineering. It solves real problems that have plagued web infrastructure for years. The current system of IP allowlists and user-agent sniffing is genuinely terrible—fragile, easily spoofed, and constantly breaking when networks change.

Having cryptographic proof of bot identity would eliminate a lot of headaches. It's already implemented in several HTTP stacks and designed to work through all the proxies and CDNs that make up the modern web.

The technical direction is right. It's the governance model that has me worried.

### Where This Could Go Wrong

Looking at the various proposals floating around, I see several ways this could end badly:

A single "universal bot registry" sounds convenient until you realize it's also a single point of control. Who decides which bots get listed? What happens when geopolitics or business disputes affect those decisions?

Some CDNs are building verification APIs optimized for their infrastructure. Cloudflare can verify at the edge, but origins can also verify locally or disable CDN verification entirely. The risk isn't technical lock-in—it's that the "easy" path might funnel everyone through a few big networks.

The private key custody thing keeps coming up in discussions, and it bothers me every time. Bot operators should own their own keys, full stop. The moment you hand that over to an intermediary "for convenience," you've lost control of your own identity.

Without transparency logs—something like Certificate Transparency but for bot identities—we'll have no way to audit who's being excluded or why. That's a recipe for abuse.

And here's the big one: identity verification shouldn't dictate policy. Knowing *who* made a request is different from deciding *what* to do with it. But once those two things get bundled together in the same service, the distinction tends to disappear.

---

### How to Do This Right

After listening to the debates in Montreal, I think there's a path forward that preserves the benefits while avoiding the worst outcomes.

**Make directories federated and auditable.** Instead of one big registry, let every bot operator host their own `/.well-known/agent-keys` endpoint with their public keys. Publishers and CDNs can choose to trust multiple directories simultaneously. Add transparency logs so we can audit what's happening—no secret exclusions, no opaque business deals affecting technical access.

**Keep verification libraries open and interoperable.** The same signature verification should work identically across Cloudflare, Akamai, NGINX, Envoy, and whatever framework you're running in your app. We already made this mistake with TLS certificate authorities—let's not repeat it by letting a few players control both issuance and validation.

**Define clear anti-replay profiles.** Give sites options for how strict they want to be about replay protection—nonces and short TTLs for high-security scenarios, more relaxed rules for basic verification. Make it configurable without breaking the intermediaries that keep the web running.

**Keep identity separate from policy.** The identity layer should just answer "who made this request?" The policy layer—allow, deny, throttle, charge—should be completely separate and competitive. Mixing them is how we accidentally hand control of the web to whoever runs the biggest edge network.

**Make onboarding trivial.** There should be a "Hello, Verified Bot" tutorial that gets you up and running in ten minutes on your laptop. If you need to negotiate an enterprise contract just to verify your crawler's identity, the system has already failed.

### What Success Looks Like

In five years, I want to see a web where bots sign every request with keys they control, sites can verify those signatures using multiple trust anchors, and policy decisions about access and pricing remain open and competitive.

The IETF should define the plumbing, not the permissions. CDNs should compete on performance and features, not on who they allow to speak.

If we get this right, the web stays composable and auditable. If we get it wrong, we'll wake up in a world where a handful of infrastructure companies quietly control the identity layer for everything that touches the open internet.

---

*This is based on my notes from IETF 124 in Montreal. The working group is still evolving these proposals, so details will change. But the fundamental tension between technical capability and governance control isn't going anywhere.*

*If you're working on web infrastructure or bot authentication, I'd love to hear your thoughts. Find me at [@hammadtariq](https://twitter.com/hammadtariq).*  
