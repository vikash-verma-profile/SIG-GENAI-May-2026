"""Gold: business aggregates."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum


def run_gold(spark: SparkSession, silver_path: Path, gold_path: Path) -> None:
    gold_path.mkdir(parents=True, exist_ok=True)
    df_clean = spark.read.parquet(str(silver_path))
    df_gold = df_clean.groupBy("diagnosis").agg(spark_sum("billing_amount").alias("total_billing"))
    df_gold.write.mode("overwrite").parquet(str(gold_path))
