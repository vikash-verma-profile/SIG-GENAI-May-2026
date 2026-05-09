# Lab 9 — AI-generated Azure DevOps pipeline (manufacturing IoT)

**Domain:** Manufacturing IoT  
**Goal:** Define an **Azure DevOps** YAML pipeline that builds Python, runs tests, builds **Docker**, and outlines **Kubernetes** deployment—typically drafted with AI then hardened by you.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `azure-pipelines.yml` | Multi-stage pipeline: Python CI → Docker build → K8s placeholder. |
| `iot_transform.py` | Sample transform logic. |
| `tests/test_iot_transform.py` | pytest coverage for CI. |
| `Dockerfile` | Container image wrapping the project (extend as needed). |
| `requirements.txt` | Includes **flake8**, **pytest**, **pandas** for pipeline stages. |
| `pytest.ini` / `.flake8` | Local and CI-friendly test/lint config. |

---

## Prerequisites

- **Azure DevOps** organization and project.
- A **repository** (Azure Repos or GitHub linked to Azure DevOps).
- Optional: **Container registry** and **Kubernetes** service connection for real deploys.

---

## Step-by-step

### 1. Create an Azure Repos project (or connect GitHub)

Push this folder’s contents to the remote configured in Azure DevOps.

### 2. Add `azure-pipelines.yml` at repo root

This lab already includes the file. In Azure DevOps:

- **Pipelines** → **New pipeline** → select repo → choose **Existing Azure Pipelines YAML file**.

### 3. AI prompt (pipeline drafting)

Example:

> Generate Azure DevOps YAML for Python 3.11: install requirements, flake8, pytest with coverage, Docker build, and a Kubernetes deployment stage placeholder using kubectl apply.

Compare AI output with `azure-pipelines.yml` and merge carefully.

### 4. Validate locally first

```bash
cd lab-9
pip install -r requirements.txt
flake8 .
pytest --cov=.
```

### 5. Docker build (local smoke test)

```bash
docker build -t manufacturing-iot-etl:local .
```

### 6. Wire Azure DevOps tasks

- Replace the **Docker@2** inputs with your registry (`containerRegistry`, `repository`) when ready.
- Replace the deployment script with real **`kubectl`** or **Helm** tasks once a cluster service connection exists.

### 7. Run the pipeline

Commit, push, run pipeline, inspect logs for each stage.

---

## Expected results

- Green **build + test** stage on agents.
- Docker image produced (or clear errors to fix).
- Deployment stage either integrated or intentionally stubbed with documented next steps.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| Pool `ubuntu-latest` unavailable | Pick another Microsoft-hosted pool per org policy. |
| Docker task auth failures | Configure service connection + ACR permissions. |
| K8s deploy skipped | Expected until cluster **Environment** + **approval** + **service connection** exist. |

---

## Learning outcomes

- Translating AI-written YAML into **org-compliant** pipelines.
- Seeing how **CI**, **containers**, and **deploy** stages compose.
