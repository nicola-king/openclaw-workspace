Halcyon

* [Platform](#bento)
* [Metrics](#metrics)
* [Docs](#docs)
* [Changelog](#changelog)

Get started

Series A · 2026 · Bordeaux

# Calmer infrastructure for the agents already running your business.

Halcyon is a runtime for long-running AI agents that need stable identity, predictable cost, and an audit trail you can hand to legal. We replace the YAML scaffolding teams keep rebuilding from scratch.

Open the console

Read the runtime spec

runtime · live

#### research-agent / tier-3

healthy · 7d 14h uptime

spend / 24h

$47.18USD

tasks / 24h

1,284ok

audit · last entry

`04:12:09` · ticket `PRD-4731` dispatched to **research-agent/tier-3** by **quentin.albrecht**. Resolved in 41.7s.

02 · platform

Five primitives. No agent framework lock-in. Bring your own model, your own tools, your own sandbox — keep the runtime, the policies, and the bill in one place.

## The runtime is the boring part. We're *obsessed* with the boring part.

01 · identity

### Stable identities, not session tokens.

Every agent gets a long-lived identity with revocable credentials, scoped policies, and a portable memory layer that survives model swaps. Rotate keys without re-onboarding the agent.

// stable across model swaps
agent.identity = {
  id: "agent\_q7\_research",
  policy: "tier-3:read-only",
  memory: halcyon.memory("q7"),
};

02 · spend

### One bill. One cap. One alarm.

Set budgets per agent, per workspace, per provider. Halcyon throttles before the bill becomes a Slack post-mortem.

$0.018avg / task

03 · audit

### An audit log shaped like an audit log.

Append-only. Cryptographically chained. Streams to your SIEM. Every tool call, every prompt, every model swap, every refund — in one place legal can actually subpoena.

04 · sandbox

### Real sandboxes.

Firecracker microVMs per task. Boots in 110ms.

05 · routing

### Model-agnostic routing.

Cheapest model that passes your eval. Updated nightly.

06 · ergonomics

### Three SDKs. Two CLIs.

Python, TypeScript, Go. `halcyon` & `hl`.

Anthropic*·*Stripe*·*Linear*·*Vercel*·*Cursor*·*Brex*·*Ramp*·*Replicate*·*Hex*·*Notion*·*
Anthropic*·*Stripe*·*Linear*·*Vercel*·*Cursor*·*Brex*·*Ramp*·*Replicate*·*Hex*·*Notion*·*

## Less duct tape between the model and the bill.

14-day evaluation, then choose pay-as-you-go or annual. We'll send a real engineer for setup. No SDR funnel.

Talk to an engineer

Halcyon Runtime · SOC 2 · ISO 27001 · v2026.05
Docs · Changelog · Status · Privacy · Contact