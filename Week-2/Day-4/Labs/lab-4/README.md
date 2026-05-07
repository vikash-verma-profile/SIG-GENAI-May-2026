# Lab 4 — README & Technical Design Doc Generation

## What you have to do (from `Lab 4.docx`)

Scenario: a logistics company has a package tracking microservice with **no documentation**, so onboarding is slow.

You will use GenAI to produce:
- A professional `README.md`
- A Technical Design Document (TDD)
- An “architecture explanation” for a new team member

The example project structure from the lab:

```
tracking-service/
│
├── app.py
├── tracking/
├── database/
├── Dockerfile
├── requirements.txt
└── kubernetes/
```

## What’s included in this folder

This lab folder contains a small runnable skeleton called `tracking-service/` so you can:
- point AI at real files
- generate README/TDD from actual code and manifests

## Task 1 — README generation prompt (use this)

> Generate a professional README.md for the following Python microservice project.
>
> Include:
> 1. Project overview
> 2. Features
> 3. Setup instructions
> 4. API endpoints
> 5. Docker deployment
> 6. Kubernetes deployment
> 7. Troubleshooting
> 8. Architecture summary

## Task 2 — TDD generation prompt (use this)

> Create a technical design document for a logistics tracking microservice.
>
> Include:
> - Architecture
> - Components
> - APIs
> - Database design
> - Deployment architecture
> - Security considerations
> - Scalability strategy

## Task 3 — Architecture explanation

Ask:
- “Explain this logistics microservice architecture to a new engineering team member.”

## Deliverables checklist

- [ ] `tracking-service/README.md`
- [ ] `TDD.md` (or `TECHNICAL_DESIGN.md`)
- [ ] Architecture explanation notes (markdown)

