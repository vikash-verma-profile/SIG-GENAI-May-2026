# Confluence Page Draft — `customer_sales_ingestion`

## Pipeline overview

- **Pipeline name**: `customer_sales_ingestion`
- **Purpose**: Ingest customer sales data from SAP HANA into Snowflake for reporting and downstream analytics.
- **Owner**: Data Engineering Team

## Source system

- **System**: SAP HANA
- **Extraction**: Incremental (recommended) with watermarking; full refresh only when necessary.

## Target system

- **System**: Snowflake
- **Target tables**: (fill) `RAW.CUSTOMER_SALES_*` / `STG.CUSTOMER_SALES_*`

## Schedule & SLA

- **Schedule**: Every 30 minutes
- **SLA**: 15 minutes (data should be available in target within 15 minutes after schedule trigger)

## Data quality rules

- No null customer IDs
- Sales amount > 0

## Monitoring process

- Monitor pipeline run status and duration
- Track row counts and anomaly detection (sudden drop/spike)
- Alert on:
  - SLA breach (runtime > 15 minutes)
  - consecutive failures
  - data quality validation failures

## Failure handling

- **Transient source outage**: retry with exponential backoff; alert on repeated failures
- **Schema changes**: detect schema drift; route to quarantine; alert owner
- **Target load failure**: rollback transaction; re-run idempotently

## Contacts / escalation

- **Primary**: Data Engineering Team (on-call)
- **Secondary**: Platform SRE (if infra-related)

