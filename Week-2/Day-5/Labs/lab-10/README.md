# Lab 10 — AI-based anomaly detection (smart city traffic analytics)

**Domain:** Smart city traffic / IoT analytics  
**Goal:** Combine **metric datasets**, simple **statistical anomaly** checks, and **LLM-assisted** interpretation for operational recommendations.

**Architecture (conceptual):** IoT sensors → Kafka → Databricks → Grafana.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `metrics.csv` | Timestamp + latency samples including a clear spike. |
| `anomaly_check.py` | Flags high latency vs **median** (robust for tiny samples). |
| `requirements.txt` | `pandas` for the script. |

---

## Prerequisites

- Python **3.10+**.
- Optional: LLM access for the qualitative part of the lab.

---

## Step-by-step

### 1. Inspect the metrics file

Open `metrics.csv`. You should see baseline latencies near **200–210** and a spike at **900**.

### 2. Run the anomaly script

```bash
cd lab-10
pip install -r requirements.txt
python anomaly_check.py
```

The script prints rows where **`latency > 3 * median`** (tunable rule for demonstration).

### 3. LLM prompt — anomaly narrative

Paste `metrics.csv` contents into your LLM with a prompt such as:

> Identify anomalies in these traffic analytics metrics. Explain likely operational causes and mitigations (Kafka consumers, Spark executors, etc.).

### 4. Compare outputs

- **Script:** deterministic flagging of the spike row.
- **LLM:** qualitative story (scaling, hotspots, downstream effects).

### 5. Document recommendations

From the lab narrative, examples include:

- Scale **Kafka consumers** for lagging partitions.
- Increase **Spark executors** if processing latency drives end-to-end delay.

Adapt wording to your actual platform.

---

## Expected results

- Detected spike aligned with human intuition (900 vs ~200).
- Written recommendations that tie metrics to **capacity** actions.

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| Too many false positives | Raise multiplier (e.g., `> 4 * median`) or switch to rolling z-score with more points. |
| Too few points | Prefer domain thresholds (SLA max latency) when sample size is tiny. |

---

## Learning outcomes

- Pairing **simple detectors** with **LLM explanation** for ops workflows.
- Recognizing **telemetry gaps** (need more rows, labels, or traces).
