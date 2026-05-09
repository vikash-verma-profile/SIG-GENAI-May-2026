# Lab 5 — Grafana AI Assist dashboard generation (logistics)

**Domain:** Logistics tracking  
**Goal:** Use **Grafana** (and optionally **Grafana AI Assist** / dashboard assistants) to design observability around deliveries and API latency.

**Architecture (conceptual):** Prometheus → Grafana.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `docker-compose.yml` | Runs Grafana locally on port **3000**. |
| `dashboard-template.json` | Skeleton JSON describing panels you can recreate or adapt in Grafana. |

---

## Prerequisites

- **Docker** (Docker Desktop on Windows, or Docker Engine on Linux).
- Browser.

---

## Step-by-step

### 1. Start Grafana

From `lab-5`:

```bash
docker compose up -d
```

Wait until the container is healthy. Open:

- `http://localhost:3000`

Default credentials in this compose file:

- User: **admin**
- Password: **admin**

Change the password when Grafana prompts you.

### 2. Connect Prometheus (lab exercise)

In Grafana:

1. **Connections** → **Data sources** → **Add data source** → **Prometheus**.
2. Set the URL to your Prometheus server (course lab may provide one; local example is often `http://host.docker.internal:9090` from inside containers—adjust per environment).

If you do not have Prometheus yet, complete the UI wiring steps conceptually or use **TestData** datasource for layout practice only.

### 3. Use AI Assist (product-dependent)

In Grafana’s Explore or dashboard builder, use **AI Assist** (wording varies by version) with a prompt such as:

> Create a dashboard with panels for: failed deliveries rate, API latency (p95), route processing failures.

Review suggested queries and panel types; adjust PromQL to match your metric names.

### 4. Build panels

Align panels with logistics KPIs:

- **Failed deliveries** — counter or rate from business metrics.
- **API latency** — histogram or gauge (p50/p95).
- **Route processing failures** — errors by route or region.

### 5. Export dashboard JSON

In Grafana:

- **Dashboard settings** → **JSON Model** → copy, or **Share** → **Export**.

Compare with `dashboard-template.json` in this folder.

---

## Expected results

- Running Grafana UI locally.
- At least a **draft dashboard** concept tied to Prometheus metrics (or placeholders documented).
- Exported JSON you could commit or share.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| Port 3000 busy | Edit `docker-compose.yml` to map `3001:3000` and open `localhost:3001`. |
| Cannot reach Prometheus | Verify Prometheus URL, firewall, and Docker networking (`host.docker.internal` on Windows/Mac). |

### Stop Grafana

```bash
docker compose down
```

---

## Learning outcomes

- Linking **SLO-style** dashboards to real metric names.
- Using AI to **bootstrap** dashboards while you validate queries.
