# Lab 2 — Bug Diagnosis Using Stack Traces (Java)

## What you have to do (from `Lab 2.docx`)

Scenario: a **healthcare appointment booking** platform crashes during peak traffic and doctors can’t view schedules.

You will:
- Analyze a production stack trace
- Use GenAI (Claude/GPT) for debugging / RCA
- Identify the root cause and fix
- Suggest observability improvements for Spring Boot on Kubernetes

## Part A — Analyze the stack trace

Error log (from the lab):

```
java.lang.NullPointerException: Cannot invoke "Doctor.getAvailability()" because "doctor" is null
    at com.healthcare.scheduler.ScheduleService.bookAppointment(ScheduleService.java:82)
    at com.healthcare.scheduler.ScheduleController.book(ScheduleController.java:44)
```

### Likely root cause

`doctorRepository.findDoctor(doctorId)` returned `null`, then code calls `doctor.getAvailability()`.

## Part B — Ask Claude/GPT (use this exact prompt)

> Analyze the following Java stack trace.
>
> Identify:
> 1. Root cause
> 2. Potential coding mistake
> 3. Recommended fix
> 4. Preventive engineering improvements
> 5. Monitoring recommendations
>
> Provide corrected code.

## Part C — Fix the faulty code (starter code in this folder)

Open `ScheduleService.java` and apply the safe null-handling fix:
- If doctor is missing, throw a domain exception
- Avoid `Boolean` null pitfalls (`Boolean.TRUE.equals(...)`)

## Part D — Observability suggestions (what to ask AI)

Ask AI:
- “Suggest observability improvements for diagnosing Java Spring Boot failures in Kubernetes.”

Expected recommendations (from the lab):
- Distributed tracing (OpenTelemetry)
- Centralized logging (structured JSON)
- Grafana dashboards + alerting
- Correlation IDs
- Exception tracking and SLOs

## Deliverables checklist

- [ ] RCA document (markdown)
- [ ] Fixed code (`ScheduleService.java`)
- [ ] AI-generated debugging summary (markdown)
- [ ] Observability recommendations (markdown)

