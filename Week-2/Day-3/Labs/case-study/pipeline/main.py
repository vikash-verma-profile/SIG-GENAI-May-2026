"""Smart agriculture medallion pipeline (PySpark + watermark + alerts)."""
import argparse
from pathlib import Path

import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, broadcast, col, sum as spark_sum, when

ROOT = Path(__file__).resolve().parent.parent


def load_config() -> dict:
    cfg_path = Path(__file__).resolve().parent / "config.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_watermark(path: Path, default: str) -> None:
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(default, encoding="utf-8")


def read_watermark(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def write_watermark(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def run(cfg: dict, stages: list[str] | None = None) -> None:
    if stages is None:
        stages = ["bronze", "silver", "gold"]

    spark = SparkSession.builder.appName(cfg["app_name"]).master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    data_dir = ROOT / cfg["data_dir"]
    bronze_path = ROOT / cfg["bronze_path"]
    silver_path = ROOT / cfg["silver_path"]
    gold_path = ROOT / cfg["gold_path"]
    watermark_path = ROOT / cfg["watermark_path"]

    ensure_watermark(watermark_path, cfg["initial_watermark"])

    try:
        if "bronze" in stages:
            bronze_path.mkdir(parents=True, exist_ok=True)
            df1 = spark.read.option("header", True).option("inferSchema", True).csv(str(data_dir / "sensor_day1.csv"))
            df2 = spark.read.option("header", True).option("inferSchema", True).csv(str(data_dir / "sensor_day2.csv"))
            combined = df1.unionByName(df2, allowMissingColumns=True)
            last_wm = read_watermark(watermark_path)
            incremental = combined.filter(col("timestamp") > last_wm)
            incremental.write.mode("overwrite").parquet(str(bronze_path))

        if "silver" in stages:
            silver_path.mkdir(parents=True, exist_ok=True)
            df = spark.read.option("mergeSchema", True).parquet(str(bronze_path))
            df_clean = df.fillna({"moisture": 0, "temperature": 0, "humidity": 0})
            df_clean = df_clean.filter(col("temperature") > 0)
            df_clean.write.mode("overwrite").partitionBy("field_id").parquet(str(silver_path))

        if "gold" in stages:
            gold_path.mkdir(parents=True, exist_ok=True)
            df_clean = spark.read.parquet(str(silver_path))
            fields = spark.read.option("header", True).option("inferSchema", True).csv(str(data_dir / "fields.csv"))

            enriched = df_clean.join(broadcast(fields), "field_id", "left")

            alerts = enriched.withColumn(
                "alert",
                when(col("temperature") > 35, "High Temp")
                .when(col("moisture") < 40, "Low Moisture")
                .otherwise("Normal"),
            )

            summary = alerts.groupBy("field_id").agg(
                avg("temperature").alias("avg_temperature"),
                avg("moisture").alias("avg_moisture"),
                spark_sum(when(col("alert") != "Normal", 1).otherwise(0)).alias("alert_events"),
            )

            alerts.write.mode("overwrite").parquet(str(gold_path / "alerts"))
            summary.write.mode("overwrite").parquet(str(gold_path / "field_summary"))

            max_ts = enriched.selectExpr("max(timestamp) as m").collect()[0]["m"]
            if max_ts is not None:
                write_watermark(watermark_path, str(max_ts))

            alerts.show()
            summary.show()

        print("Completed stages:", ", ".join(stages))
    finally:
        spark.stop()


def main() -> None:
    cfg = load_config()
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", action="append", choices=["bronze", "silver", "gold"])
    args = parser.parse_args()
    run(cfg, args.stage)


if __name__ == "__main__":
    import sys

    cfg = load_config()
    if "--stage" in sys.argv:
        main()
    else:
        run(cfg, None)
