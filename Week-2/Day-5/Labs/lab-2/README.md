# Lab 2 — AI-generated GitHub Actions CI/CD for healthcare ETL

**Domain:** Healthcare claims processing  
**Goal:** Use AI to produce a **GitHub Actions** workflow that lints, tests, and reports coverage on pull requests.

**Architecture (conceptual):** Hospital DB → Python ETL → Azure SQL.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Workflow: PR trigger, Python setup, install deps, **flake8**, **pytest --cov**. |
| `pipeline/claims_transform.py` | Small example transform for CI to exercise. |
| `tests/test_claims_transform.py` | pytest unit test. |
| `requirements.txt` | `flake8`, `pytest`, `pytest-cov`, `pandas`. |
| `pytest.ini` | Resolves imports for `pipeline`. |
| `.flake8` | Lint rules (line length, excludes). |

---

## Prerequisites

- Git installed.
- A **GitHub** repository (empty or existing).
- Python **3.11** recommended.

---

## Step-by-step

### 1. Initialize Git and connect remote (if starting fresh)

```bash
git init
git remote add origin <your-repo-url>
```

Replace `<your-repo-url>` with your HTTPS or SSH URL.

### 2. Workflow folder

This repo already contains `.github/workflows/`. If you recreate manually:

```bash
mkdir -p .github/workflows
```

(On Windows PowerShell you can use `New-Item -ItemType Directory -Force -Path .github/workflows`.)

### 3. AI prompt (workflow generation)

Example prompt:

> Generate a GitHub Actions workflow for Python ETL: trigger on pull requests, use Ubuntu, checkout, setup Python 3.11, `pip install -r requirements.txt`, run **flake8** on the repo, run **pytest** with coverage.

Compare with `ci.yml` in this lab.

### 4. Install and verify locally

From this folder (`lab-2`):

```bash
pip install -r requirements.txt
flake8 .
pytest --cov=.
```

Fix any lint or test failures before pushing.

### 5. Push to GitHub

```bash
git add .
git commit -m "Add CI pipeline for healthcare ETL"
git push -u origin main
```

Use your default branch name if it is not `main`.

### 6. Validate on GitHub

1. Open the repository on GitHub.
2. Go to **Actions**.
3. Open a **pull request** that touches the workflow or Python files and confirm the workflow runs.

---

## Expected results

- CI runs on **pull_request**.
- **flake8** fails the job on style violations (configure `.flake8` if needed).
- **pytest --cov=.** produces coverage in the Actions log.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| Workflow not listed | Ensure YAML is under `.github/workflows/` and committed. |
| `flake8` fails on generated/cache dirs | Extend `exclude` in `.flake8`. |
| Wrong Python version | Edit `python-version` under `actions/setup-python@v5`. |

---

## Learning outcomes

- Reading and trusting-but-verifying **AI-generated YAML**.
- **GitHub Actions** as automated gate for Python data pipelines.
