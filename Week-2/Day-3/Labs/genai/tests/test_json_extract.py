import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from json_extract import extract_json_object  # noqa: E402


def test_extract_plain_json():
    assert extract_json_object('{"a": 1}') == {"a": 1}


def test_extract_json_embedded_in_text():
    text = 'Here you go:\n{"ok": true, "x": 3}\nThanks.'
    assert extract_json_object(text) == {"ok": True, "x": 3}
