"""Lab 2 starter: FastAPI metadata service — extend with AI."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Banking Pipeline Metadata API",
    version="0.1.0",
)


class PipelineRecord(BaseModel):
    pipeline_id: str
    status: str
    last_run: datetime
    row_count: int = 0


class AlertCreate(BaseModel):
    pipeline_id: str = Field(..., description="Pipeline identifier")
    severity: Literal["info", "warning", "critical"] = "warning"
    message: str


# In-memory store for the lab (replace with DB / file in production)
_PIPELINES: list[dict[str, Any]] = [
    {
        "pipeline_id": "core_etl",
        "status": "Success",
        "last_run": datetime(2026, 5, 7, 9, 0, 0),
        "row_count": 420000,
    },
    {
        "pipeline_id": "risk_etl",
        "status": "Failed",
        "last_run": datetime(2026, 5, 7, 9, 12, 0),
        "row_count": 0,
    },
]

_ALERTS: list[dict[str, Any]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/pipelines", response_model=list[PipelineRecord])
def list_pipelines() -> list[PipelineRecord]:
    return [PipelineRecord(**row) for row in _PIPELINES]


@app.get("/pipelines/{pipeline_id}", response_model=PipelineRecord)
def get_pipeline(pipeline_id: str) -> PipelineRecord:
    for row in _PIPELINES:
        if row["pipeline_id"] == pipeline_id:
            return PipelineRecord(**row)
    raise HTTPException(status_code=404, detail="Pipeline not found")


@app.post("/alerts", status_code=201)
def create_alert(body: AlertCreate) -> dict[str, Any]:
    record = {
        "pipeline_id": body.pipeline_id,
        "severity": body.severity,
        "message": body.message,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _ALERTS.append(record)
    return record


@app.get("/alerts")
def list_alerts() -> list[dict[str, Any]]:
    return list(_ALERTS)
