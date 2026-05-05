import os

import requests

OLLAMA_URL = os.environ.get(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate",
)
CONNECT_TIMEOUT_S = float(os.environ.get("OLLAMA_CONNECT_TIMEOUT", "5"))
READ_TIMEOUT_S = float(os.environ.get("OLLAMA_READ_TIMEOUT", "300"))


def ask_llm(prompt: str, model: str | None = None) -> str:
    model = model or os.environ.get("OLLAMA_MODEL", "llama3")
    base = OLLAMA_URL.replace("/api/generate", "").rstrip("/") or "http://127.0.0.1:11434"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=(CONNECT_TIMEOUT_S, READ_TIMEOUT_S),
        )
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"Cannot reach Ollama at {base}. Start the Ollama app or run "
            f"`ollama serve`, then `ollama pull {model}` if needed."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama did not respond in time (first run loads the model into RAM "
            f"and can exceed {READ_TIMEOUT_S:.0f}s). Raise OLLAMA_READ_TIMEOUT if needed."
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        response.raise_for_status()
        raise RuntimeError(
            f"Ollama returned non-JSON body (status {response.status_code}): "
            f"{response.text[:500]}"
        ) from exc

    if not response.ok:
        err = data.get("error", data)
        raise RuntimeError(f"Ollama HTTP {response.status_code}: {err}")

    if "error" in data and "response" not in data:
        raise RuntimeError(f"Ollama error: {data['error']}")

    if "response" not in data:
        raise RuntimeError(
            f"Unexpected Ollama JSON (no 'response' key): {data}"
        )

    return data["response"]
