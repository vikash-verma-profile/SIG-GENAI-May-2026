# Lab 4 — Technical Design Document (TDD) Starter

## Overview

`tracking-service` is a small HTTP microservice for creating and fetching package tracking status.

## Architecture

- **API layer**: Flask (`app.py`)
- **Service layer**: business logic (`tracking/service.py`)
- **Data access**: DB abstraction (`database/db.py`)
- **Deployment**: Docker + Kubernetes manifests under `tracking-service/kubernetes/`

## Components

- **`TrackingService`**: validates/normalizes inputs and stores a tracking record
- **`TrackingDB`** interface: allows swapping in PostgreSQL/Redis later
- **`InMemoryTrackingDB`**: simple reference implementation for the lab

## API design

- `POST /tracking`: upsert a tracking record
- `GET /tracking/<tracking_id>`: read a record
- `GET /health`: health probe

## Data model

`TrackingRecord`:
- `tracking_id` (string, unique)
- `status` (string, e.g., CREATED/IN_TRANSIT/DELIVERED)
- `location` (optional string)

## Deployment architecture

- Container image built from `Dockerfile`
- Kubernetes Deployment + Service
- Horizontal scaling: replicas (start at 2)

## Security considerations

- Input validation for required fields
- Add auth (JWT/OAuth) for write endpoints in production
- Add rate limiting and request size limits
- Ensure secrets are stored in K8s secrets (not in code)

## Scalability strategy

- Replace in-memory DB with PostgreSQL
- Add cache (Redis) for frequently read tracking IDs
- Add async event pipeline (Kafka) for status updates from carriers
- Autoscale based on CPU/RPS and queue depth (if async)

## Monitoring & reliability

- Metrics: latency p95/p99, 4xx/5xx rates
- Logs: structured JSON, request IDs
- Tracing: OpenTelemetry instrumentation
- Health checks: `/health` for liveness/readiness

