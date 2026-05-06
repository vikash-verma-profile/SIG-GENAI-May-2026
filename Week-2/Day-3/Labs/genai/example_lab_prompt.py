"""
Example: call Ollama from Python with a lab-style prompt.

Prerequisites:
- `ollama serve` running locally (default http://127.0.0.1:11434)
- Model pulled, e.g. `ollama pull llama3`

Run from repo root or from this folder:

    cd Labs/genai
    python example_lab_prompt.py

Override model/host:

    set OLLAMA_MODEL=qwen2.5-coder
    set OLLAMA_HOST=http://127.0.0.1:11434
    python example_lab_prompt.py
"""

from __future__ import annotations

import os

from ollama_client import generate


def main() -> None:
    model = os.environ.get("OLLAMA_MODEL", "llama3")
    prompt = """\
You are helping with a GenAI-for-data-engineering lab.

Context:
- Input CSV columns: patient_id, name, age, diagnosis, visit_date, billing_amount
- Goals: remove duplicates, fill missing age with mean age, fill missing billing_amount with 0,
  compute total billing per diagnosis, compute daily patient counts.

Task:
1) Outline the pandas steps (functions + order).
2) List 3 validation checks we should encode as tests.

Keep the answer concise (bullets).
"""
    text = generate(
        prompt,
        system="Answer clearly for a student lab. Do not invent libraries beyond pandas unless necessary.",
        model=model,
    )
    print(text)


if __name__ == "__main__":
    main()
