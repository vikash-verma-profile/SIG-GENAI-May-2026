from pathlib import Path

import yaml


def test_config_loads():
    cfg_path = Path(__file__).resolve().parent.parent / "pipeline" / "config.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert cfg["app_name"]
