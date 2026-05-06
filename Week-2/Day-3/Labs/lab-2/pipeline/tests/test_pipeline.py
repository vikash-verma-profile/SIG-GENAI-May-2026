"""Smoke tests (avoid spinning Spark in CI unless pyspark is available)."""
from pathlib import Path

import yaml


def test_config_exists():
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "settings.yaml"
    assert cfg_path.is_file()


def test_config_loads():
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "settings.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert cfg["app_name"]
    assert cfg["bronze_path"]
