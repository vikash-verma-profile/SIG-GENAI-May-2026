"""Offline tests (mock Ollama HTTP)."""

from __future__ import annotations

import json
from unittest.mock import patch

from ollama_client import chat


def test_chat_parses_message_content():
    fake_body = json.dumps(
        {
            "model": "test-model",
            "created_at": "...",
            "message": {"role": "assistant", "content": "hello"},
            "done": True,
        }
    ).encode("utf-8")

    class FakeResp:
        def read(self):
            return fake_body

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    with patch("urllib.request.urlopen", return_value=FakeResp()):
        out = chat([{"role": "user", "content": "ping"}], model="test-model")

    assert out == "hello"
