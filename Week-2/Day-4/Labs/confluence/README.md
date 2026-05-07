# Confluence / Notion Draft Generation (Pipeline Metadata → Docs)

## What you have to do (from `Confluence.docx`)

Scenario: a data engineering platform has 200+ pipelines and no documentation.
You will use GenAI to generate:
- Confluence page drafts from pipeline metadata
- Notion-ready knowledge base pages/templates
- Governance documentation summaries

## Sample pipeline metadata (from the lab)

```json
{
  "pipeline_name": "customer_sales_ingestion",
  "source": "SAP HANA",
  "target": "Snowflake",
  "schedule": "Every 30 minutes",
  "owner": "Data Engineering Team",
  "sla": "15 minutes",
  "data_quality_rules": [
    "No null customer IDs",
    "Sales amount > 0"
  ]
}
```

## Task 1 — Confluence draft prompt (use this)

> Generate a Confluence documentation page from the following pipeline metadata.
>
> Include:
> - Pipeline overview
> - Source and target systems
> - SLA
> - Data quality rules
> - Monitoring process
> - Failure handling
> - Contact information

## Task 2 — Notion knowledge base prompt

Ask AI:
- “Create a Notion-ready operational knowledge page for this data pipeline.”

## Deliverables

- [ ] `CONFLUENCE_DRAFT.md`
- [ ] `NOTION_KB_PAGE.md`
- [ ] Governance template / checklist

