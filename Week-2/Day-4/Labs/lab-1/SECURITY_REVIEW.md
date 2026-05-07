# Lab 1 — Vulnerability Report & Remediation Checklist

## Vulnerability report (based on the vulnerable sample in `Lab 1.docx`)

### Security vulnerabilities

- **SQL injection**: building SQL with string interpolation allows attackers to manipulate the query.
- **Hardcoded database credentials**: credentials embedded in code leak via repo access/logs and are hard to rotate.
- **Plain-text password check**: comparing `password` in SQL implies passwords are stored/validated in plain text.
- **No brute-force protection**: no rate limiting / account lockout / IP throttling.
- **No secure authentication mechanism**: no session management/JWT; no token expiry strategy.
- **Weak error handling**: exceptions can crash requests and leak internals via stack traces.

### Performance / reliability issues

- **DB connection per request**: expensive connection setup increases latency and can exhaust DB under load.
- **No pooling**: increases connection churn and failures during traffic spikes.
- **No caching**: frequent reads (e.g., user auth lookups) can be cached with short TTL where appropriate.
- **No timeouts**: DB/network calls without timeouts can hang, increasing resource usage.

## Recommended secure fixes (what “good” looks like)

- **Use parameterized queries** (`WHERE username=%s`) and pass parameters separately.
- **Use password hashes** (store `password_hash`, validate with a secure hash function).
- **Move secrets to environment** (Kubernetes secrets, `.env` in local dev).
- **Connection pooling** (e.g., `psycopg2.pool.SimpleConnectionPool`).
- **Rate limiting** on `/login` and other sensitive endpoints.
- **JWT** (or a session mechanism) with expiry, issuer, and secret management.

## Remediation checklist

- [ ] Remove hardcoded DB creds; use env vars and secret manager
- [ ] Replace dynamic SQL string building with parameterized SQL
- [ ] Store passwords hashed (never plaintext); validate with secure hashing
- [ ] Add rate limiting / brute force controls
- [ ] Add structured error handling (avoid leaking internals)
- [ ] Add DB connection pooling and safe cleanup
- [ ] Add Redis caching where it improves latency and doesn’t create security issues
- [ ] Add observability: request IDs, structured logs, metrics (latency, error rate, DB pool usage)

