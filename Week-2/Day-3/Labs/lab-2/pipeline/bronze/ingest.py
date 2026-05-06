"""Bronze: raw CSV ingestion to Parquet."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def run_bronze(spark: SparkSession, csv_path: Path, bronze_path: Path, last_run_date: str) -> None:
    bronze_path.mkdir(parents=True, exist_ok=True)
    try:
        df = spark.read.option("header", True).option("inferSchema", True).csv(str(csv_path))
    except Exception as e:
        raise RuntimeError(f"Error loading CSV into bronze: {e}") from e

    df_incremental = df.filter(col("visit_date") > last_run_date)
    # Lab doc shows append for incremental loads; overwrite keeps reruns reproducible locally.
    df_incremental.write.mode("overwrite").parquet(str(bronze_path))
