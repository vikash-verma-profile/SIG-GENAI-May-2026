"""Healthcare medallion pipeline entrypoint (optional Ollama watermark suggestion)."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml
from pyspark.sql import SparkSession

from bronze.ingest import run_bronze
from gold.aggregate import run_gold
from silver.clean import run_silver

ROOT = Path(__file__).resolve().parent.parent  # Labs/lab-2
LABS_ROOT = ROOT.parent  # Labs
if str(LABS_ROOT) not in sys.path:
    sys.path.insert(0, str(LABS_ROOT))


def load_config() -> dict:
    cfg_path = Path(__file__).resolve().parent / "config" / "settings.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def execute(stages: list[str] | None = None, cfg_override: dict | None = None) -> None:
    cfg = dict(load_config())
    if cfg_override:
        cfg.update(cfg_override)
    if stages is None:
        stages = ["bronze", "silver", "gold"]

    spark = SparkSession.builder.appName(cfg["app_name"]).master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    csv_path = ROOT / cfg["input_csv"]
    bronze_path = ROOT / cfg["bronze_path"]
    silver_path = ROOT / cfg["silver_path"]
    gold_path = ROOT / cfg["gold_path"]

    try:
        if "bronze" in stages:
            run_bronze(spark, csv_path, bronze_path, cfg["last_run_date"])
        if "silver" in stages:
            run_silver(spark, bronze_path, silver_path)
        if "gold" in stages:
            run_gold(spark, silver_path, gold_path)
        print("Stages completed:", ", ".join(stages))
        if cfg_override:
            print("Effective config overrides:", cfg_override)
    finally:
        spark.stop()


def _env_truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab-2 medallion pipeline (optional --ai watermark JSON).")
    parser.add_argument(
        "--stage",
        action="append",
        choices=["bronze", "silver", "gold"],
        help="Run only selected stage(s). Repeat flag for multiple.",
    )
    parser.add_argument("--ai", action="store_true", help="Ask Ollama for last_run_date (JSON-only).")
    parser.add_argument("--intent", default=None, help="Natural-language intent for watermark choice.")
    args = parser.parse_args()

    overlay = None
    use_ai = args.ai or _env_truthy("USE_OLLAMA_PIPELINE")
    if use_ai:
        from genai.dynamic_spec import lab2_watermark_spec, read_csv_header_line

        cfg = load_config()
        csv_path = ROOT / cfg["input_csv"]
        hdr = read_csv_header_line(csv_path)
        overlay = lab2_watermark_spec(hdr, str(cfg["last_run_date"]), args.intent)
        print("Ollama-enabled overlay:", overlay)

    stages = args.stage if args.stage else None
    execute(stages, cfg_override=overlay)


if __name__ == "__main__":
    main()
