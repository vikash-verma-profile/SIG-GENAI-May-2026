# Lab 2 — Root Cause Analysis (RCA)

## Incident summary

During peak traffic, the appointment booking backend crashes, preventing doctors from viewing schedules.

## Evidence (stack trace)

`NullPointerException`:
- `doctor` is `null`
- Code calls `doctor.getAvailability()`

## Root cause

`doctorRepository.findDoctor(doctorId)` can return `null` (doctor not found / stale cache / DB inconsistency).
The service does not validate the return value before dereferencing it.

## Fix

- Validate `doctor != null` and throw a domain exception (`DoctorNotFoundException`).
- Use `Boolean.TRUE.equals(...)` if `getAvailability()` may return `Boolean` (nullable).

See: `ScheduleService.java` in this folder.

## Preventive improvements

- Add input validation and consistent error responses at the controller layer.
- Add tests for “doctor not found” and “availability is null” paths.
- Prefer `Optional<Doctor>` return type from repositories, or enforce non-null.
- Add structured exception handling to map `DoctorNotFoundException` to `404`.

## Monitoring & observability recommendations

- Structured logs with correlation IDs (requestId/traceId).
- Distributed tracing (OpenTelemetry) across controller → service → DB/Kafka calls.
- Metrics:
  - `5xx` rate, latency p95/p99
  - “doctor not found” count (4xx) as a product signal
  - DB query latency / pool saturation
- Dashboards (Grafana) + alerts tied to SLOs.

