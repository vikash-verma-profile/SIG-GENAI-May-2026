# Lab 5 — Runbook & Incident Playbook Generation

## What you have to do (from `Lab 5.docx`)

Scenario: a telecom company experiences frequent outages in network monitoring pipelines.

Alert:
- Kafka consumer lag exceeded threshold
- Packet processing delayed by 15 minutes

You will use GenAI to generate:
- Incident response playbook (Kafka consumer lag in Kubernetes)
- Recovery runbook (restore failed monitoring services)
- Postmortem template

## Task 1 — Incident playbook prompt (use this)

> Create an incident response playbook for Kafka consumer lag issues in Kubernetes.
>
> Include:
> 1. Symptoms
> 2. Possible causes
> 3. Investigation steps
> 4. Commands to execute
> 5. Rollback procedures
> 6. Escalation matrix
> 7. SLA considerations

## Task 2 — Recovery runbook prompt (use this)

> Generate a telecom operations runbook for restoring failed monitoring services.

## Task 3 — Postmortem prompt (use this)

> Generate a postmortem template for telecom platform outages.

## Starter docs in this folder

- `INCIDENT_PLAYBOOK.md`
- `OPERATIONS_RUNBOOK.md`
- `POSTMORTEM_TEMPLATE.md`

