# Action Items — Engineering Meeting

## Action items

1) **Fix schema mismatch in ingestion pipeline**
   - **Owner**: Rahul
   - **Deadline**: Tomorrow
   - **Notes**: Update ADF mapping and validate end-to-end run.

2) **Validate Snowflake tables after mapping fix**
   - **Owner**: Priya
   - **Deadline**: Tomorrow (after Rahul’s fix)
   - **Notes**: Confirm schema alignment, row counts, and critical columns.

3) **Increase Kubernetes memory limits for affected services**
   - **Owner**: DevOps team
   - **Deadline**: Tomorrow
   - **Notes**: Update resource requests/limits; monitor for OOM events.

4) **Prepare for client demo**
   - **Owner**: Project team
   - **Deadline**: Friday
   - **Notes**: Confirm ingestion health and dashboard freshness before demo.

## Risks

- Demo risk if ingestion pipeline remains unstable.
- Regression risk from ADF mapping changes without validation.
- Resource change risk if memory limits hide leaks rather than fixing root cause.

## Follow-up reminders

- Check-in tomorrow EOD: confirm mapping fix merged + pipeline success.
- Pre-demo checklist (Thursday): pipeline green, Snowflake validation done, dashboards fresh.

