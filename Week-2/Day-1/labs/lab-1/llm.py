import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
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
