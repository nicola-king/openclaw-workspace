Northwind / Identity / Auth

# auth-service

Owned by @identity-platform · v4.7.2 · Last reviewed 14 Oct 2025

Tier 0 · production-critical

## 01Service summary

**auth-service** issues, validates, and revokes session tokens for every Northwind product surface — web, mobile, and the public API. It owns the password store, the TOTP/WebAuthn enrollments, and the audit-log writer for all auth events.

If `auth-service` is down, customers cannot log in or refresh sessions. Existing valid sessions continue to work for their TTL (15 minutes) but no new auth happens.

### Dependencies

* Postgres · auth-dbhealthy
* Redis · session-cachehealthy
* KMS · auth-keyringhealthy
* SES · transactionaldegraded
* Pager · oncall.northwindhealthy

## 02Alerts you might wake up to

| Alert | Severity | What it means | First response |
| --- | --- | --- | --- |
| auth.login\_5xx\_rate > 1% | SEV-1 | Login endpoint returning errors. Customers are locked out. | Check Postgres + Redis dashboards. Roll back last deploy if < 30 min old. |
| auth.token\_refresh\_lag\_p95 > 800ms | SEV-2 | Refresh path is slow. Web app starts to feel sluggish. | Inspect Redis CPU + connection count. Scale read replicas if needed. |
| auth.signup\_failure > 10/min | SEV-2 | New signups are failing. Often SES bounces or SMTP auth. | Check SES bounce rate. Failover transactional queue to backup region. |
| auth.kms\_signing\_errors > 0 | SEV-1 | KMS can't sign session tokens. New logins fail; existing sessions OK. | Page the security team. Do not roll keys without a security engineer. |
| auth.audit\_writer\_backlog > 5k | SEV-3 | Audit log writer is falling behind. Compliance impact. | Drain manually. Open a ticket; not a wake-up. |

## 03Common procedures

### Deploy a new version

Use during business hours

Deploys are blue/green. The script waits for two consecutive healthchecks before promoting traffic.

```
# Deploy auth-service v4.7.3 to production
$ nw deploy auth-service --tag v4.7.3 --env production

# Wait for two consecutive healthchecks (~90 s), then promote.
$ nw deploy promote auth-service --env production
→ traffic shifted: 10% / 50% / 100%
```

### Roll back to last known good

Use when error rate > 1% post-deploy

```
# Rolls back to the previously promoted version, no rebuild.
$ nw deploy rollback auth-service --env production
→ rolled back to v4.7.2 in 38 s
```

### Rotate signing keys

Schedule with security; never solo

```
# 1. Generate the new signing key in KMS
$ nw kms create-key --alias auth-signing-$(date +%Y%m%d)

# 2. Mark the new key as the primary; old key remains valid for 24h
$ nw kms set-primary auth-signing --key <arn>

# 3. After 24h, schedule deletion of the previous key
$ nw kms schedule-deletion auth-signing --key <old-arn> --days 30
```

### Drain audit-log backlog

Use when audit\_writer\_backlog alert fires

```
$ nw exec auth-service -- bin/audit-drain --batch 5000
→ drained 4,812 entries in 12 s; backlog now 0
```

## 04On-call rotation · this month

| Week | Primary | Secondary | Backup (escalation) |
| --- | --- | --- | --- |
| Oct 27 – Nov 02 | Devon Park | Priya Banerjee | Sasha Lin |
| Nov 03 – Nov 09 | Caleb Renner | Devon Park | Sasha Lin |
| Nov 10 – Nov 16 | Priya Banerjee | Caleb Renner | Mira Reddy |
| Nov 17 – Nov 23 | Sasha Lin | Priya Banerjee | Mira Reddy |

## 05Incident response — first 30 minutes

1

#### Acknowledge the page within 5 min.

Type `/ack` in `#incidents-auth`. The bot stops re-paging and tags the on-call.

2

#### Open the incident channel.

Run `/incident open auth-service "<short title>"`. Slack bot creates a dedicated channel and pages the secondary.

3

#### Post a status snapshot.

Customer-impact in one line, what you know, what you're checking next. Re-post every 10 minutes.

4

#### Mitigate before you diagnose.

If a recent deploy is suspect, roll back. If KMS is degraded, fail open is *never* the answer for auth — escalate to security.

5

#### Hand off or stand down.

If you can't resolve in 30 min, hand to the secondary. When healthy, close with `/incident close`; postmortem is owed within 5 business days.

Northwind Identity Platform · runbook v3.2
Source: ops-docs/auth-service.md