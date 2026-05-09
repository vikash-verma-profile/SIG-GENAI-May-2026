"""Lab 8 starter: ETL monitoring API (airline domain)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Airline ETL Monitor API", version="0.1.0")


class EtlJob(BaseModel):
    job_id: str
    name: str
    status: str
    last_run: datetime
    duration_sec: int
    rows_processed: int


class SlaMetric(BaseModel):
    job_id: str
    slo_seconds: int
    last_duration_sec: int
    met_sla: bool


_JOBS: list[dict[str, Any]] = [
    {
        "job_id": "pnr_extract",
        "name": "PNR nightly extract",
        "status": "success",
        "last_run": datetime(2026, 5, 7, 2, 0, 0),
        "duration_sec": 900,
        "rows_processed": 1_200_000,
    },
    {
        "job_id": "loyalty_sync",
        "name": "Loyalty sync",
        "status": "failed",
        "last_run": datetime(2026, 5, 7, 3, 15, 0),
        "duration_sec": 120,
        "rows_processed": 0,
    },
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/etl/jobs", response_model=list[EtlJob])
def list_jobs() -> list[EtlJob]:
    return [EtlJob(**j) for j in _JOBS]


@app.get("/etl/jobs/{job_id}", response_model=EtlJob)
def get_job(job_id: str) -> EtlJob:
    for j in _JOBS:
        if j["job_id"] == job_id:
            return EtlJob(**j)
    raise HTTPException(status_code=404, detail="Job not found")


@app.get("/etl/failures")
def failures() -> list[EtlJob]:
    return [EtlJob(**j) for j in _JOBS if j["status"].lower() == "failed"]


@app.get("/etl/sla", response_model=list[SlaMetric])
def sla_metrics(slo_seconds: int = Query(3600, ge=60)) -> list[SlaMetric]:
    out: list[SlaMetric] = []
    for j in _JOBS:
        dur = int(j["duration_sec"])
        out.append(
            SlaMetric(
                job_id=j["job_id"],
                slo_seconds=slo_seconds,
                last_duration_sec=dur,
                met_sla=dur <= slo_seconds,
            )
        )
    return out
