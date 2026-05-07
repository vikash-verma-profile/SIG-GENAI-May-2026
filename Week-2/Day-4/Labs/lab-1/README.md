# Lab 1 — AI Code Review (Security + Performance)

## What you have to do (from `Lab 1.docx`)

You are reviewing a **FinTech payment processing microservice** (Python Flask). Customers reported:
- Slow transaction processing
- Random server crashes
- Security audit failures

Your job is to use GenAI (Claude/GPT) to produce:
- **Vulnerability report**
- **Optimized secure code**
- **AI-generated recommendations**
- **Security remediation checklist**

## Part A — Run the (secure) sample service in this folder

### 1) Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a `.env` (or set variables in your shell):

- `DB_HOST=localhost`
- `DB_NAME=payments`
- `DB_USER=payments_app`
- `DB_PASSWORD=...`
- `JWT_SECRET=...` (required to issue tokens)
- `REDIS_URL=redis://localhost:6379/0`

### 3) Start the API

```bash
python app.py
```

### 4) Test endpoints

- Health:

```bash
curl http://localhost:5000/health
```

- Login (expects a `users` table with `username` and `password_hash`):

```bash
curl -X POST http://localhost:5000/login ^
  -H "Content-Type: application/json" ^
  -d "{ \"username\": \"alice\", \"password\": \"secret\" }"
```

## Part B — Do the AI-assisted code review (the core lab task)

### 1) Use this exact prompt (from the lab)

Paste the *vulnerable* sample code from the doc into your model and ask:

> Review the following Flask API code.
>
> Identify:
> 1. Security vulnerabilities
> 2. Performance bottlenecks
> 3. Code quality issues
> 4. Recommended fixes
> 5. Production-grade improvements
>
> Provide secure optimized code.

### 2) Produce a vulnerability report

Include at least:
- SQL injection risk (string interpolation in SQL)
- Hardcoded credentials
- Plain-text password validation
- No error handling
- No rate limiting / brute-force protection
- No auth token/session strategy

### 3) Produce performance findings

Include at least:
- DB connection per request (no pooling)
- No caching strategy (e.g., Redis)
- No async/background processing for heavy tasks
- No horizontal scaling considerations

### 4) Compare “before vs after”

Use this folder’s `app.py` as an example “after”:
- **Parameterized SQL**
- **Connection pooling**
- **Rate limiting**
- **JWT issuance (if configured)**
- **Redis usage example**
- **Structured error responses**

## Part C — AI performance analysis (from the lab)

Ask your model:
- “Identify performance anti-patterns in this Flask microservice and recommend optimization techniques for high-scale payment systems.”

Expected recommendations include:
- Redis caching
- Async processing / queues
- Connection pooling
- Horizontal scaling
- API throttling
- JWT authentication
- Kubernetes autoscaling

## Deliverables checklist

- [ ] Vulnerability report (markdown)
- [ ] Optimized secure code (this folder)
- [ ] AI-generated recommendations (markdown)
- [ ] Security remediation checklist (markdown)

