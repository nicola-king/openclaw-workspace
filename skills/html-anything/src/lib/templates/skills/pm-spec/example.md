Northwind / Specs / Auth
Draft v0.4

Owner · Devon Park
Updated · 22 Oct 2025
Reviewers · 4

# Two-factor authentication for the Northwind app.

Add TOTP and security-key second factors to the Northwind login flow so enterprise customers can meet their internal controls and we can move from "considered" to "approved" on three pending deals.

**Squad**Identity Platform
**Engineering lead**Priya Banerjee
**Design lead**Sasha Lin
**Target launch**End Q4 (Dec 18)
**Effort**~6 eng-weeks

## ProblemWhat hurts today, and for whom.

Three of the last six enterprise security reviews flagged the absence of a second factor as a blocker. Today, password is the only thing standing between a phished credential and a workspace full of customer data — for tenants under SOC 2 Type II expectations that's not just a perception problem, it's a control-plane gap.

It also affects internal staff: every engineer with prod access is on the same auth surface as a marketing-team viewer. We rely on policy, not posture.

"We love the product, but the absence of TOTP came up in two of three security reviews. Add it and we can sign."

— Maya Reddy · CTO, Pioneer Robotics

## Goals & non-goalsWhat this spec ships, and what we're explicitly leaving for later.

### ✓Goals

* TOTP support (Authy, 1Password, Google Authenticator) for all paid plans.
* Security key support (WebAuthn) for Enterprise plans.
* Workspace-level enforcement: admin can require 2FA for all members.
* Recovery codes — printable, downloadable, regeneratable.
* Audit log entries for setup, change, and removal events.

### ×Non-goals

* SMS as a second factor (NIST deprecated; not adding).
* SSO replacement — SAML stays a separate workstream.
* Per-action step-up (future spec, owned by Identity).
* Custom 2FA brand voice for whitelabel deployments.

## Success metricsWe'll judge this launch on the three numbers below at the 30 / 60 / 90 day marks.

| Metric | Baseline | Target (90d) | How we measure |
| --- | --- | --- | --- |
| Enterprise deals unblocked by 2FA gap | 0 of 3 | 3 of 3 | Sales motion notes + signed contract count |
| Member 2FA adoption (paid workspaces) | n/a | ≥ 60% | auth.factor\_enrolled events / DAU |
| Account takeover incidents (rolling 30d) | 4 last quarter | ≤ 1 | Security incident tracker (SEV-3+) |
| Support load from 2FA recovery | n/a | < 1.5% of tickets | Tagged "auth-2fa" in Zendesk |

## User storiesThree personas, three motions.

1

As a **workspace admin**, I want to require 2FA for everyone in my workspace, so that I can pass our annual SOC 2 control review.

2

As a **day-to-day member**, I want to enroll a TOTP app in under two minutes, so that I'm not pulled out of work to reconfigure auth.

3

As a **support engineer**, I want a clear path to help locked-out users without bypassing their second factor, so that we don't undo the security we just added.

## Rollout milestonesFour phases. Each phase ships behind a flag.

M1 · Nov 4

#### TOTP enrollment

2 eng-weeks

* Settings page UI
* Recovery codes
* Audit log entries

M2 · Nov 18

#### Login flow

1.5 eng-weeks

* Challenge step in login
* Trusted-device cookie
* Rate limiting

M3 · Dec 2

#### WebAuthn + admin enforcement

2 eng-weeks

* Security keys (Enterprise)
* Workspace policy
* Member nag prompt

M4 · Dec 18

#### GA + comms

0.5 eng-weeks

* Changelog + email
* Help center articles
* Sales enablement

## Open questionsAssigned. We need answers by Friday Oct 31 to keep the date.

Should we let members choose between TOTP and security keys, or pick the strongest available factor for them?

DPDevon Park · Oct 28

Trusted-device cookie lifetime: 7 days, 30 days, or admin-configurable?

PBPriya Banerjee · Oct 29

Do we surface a member's 2FA status in the admin user list, or only in the audit log?

SLSasha Lin · Oct 30

Northwind Identity Platform · spec-2fa
v0.4 · 22 October 2025