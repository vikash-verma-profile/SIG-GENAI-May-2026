# Notion Knowledge Base — Data Pipeline: `customer_sales_ingestion`

## TL;DR

Ingest customer sales data from SAP HANA to Snowflake every 30 minutes. SLA is 15 minutes.

## Ownership

- Owner: Data Engineering Team
- On-call rotation: (link)

## Run schedule

- Frequency: Every 30 minutes
- Expected duration: (fill)
- SLA: 15 minutes

## Inputs / outputs

- Source: SAP HANA
- Target: Snowflake

## Data quality

- Rule: customer_id not null
- Rule: sales_amount > 0

## Monitoring

- Dashboards: (link)
- Alerts: SLA breach, consecutive failures, DQ failures

## Common failures & fixes

- **Schema mismatch**: validate mapping; update transformation; re-run failed window
- **Source timeout**: retry; confirm SAP availability
- **Snowflake load failure**: check warehouse health; check staging files; re-run idempotently

## Contacts

- Data Engineering Team: (slack/email)
- SRE: (slack/email)

