"""Silver: clean bronze data with schema merge support."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean


def run_silver(spark: SparkSession, bronze_path: Path, silver_path: Path) -> None:
    silver_path.mkdir(parents=True, exist_ok=True)
    df = spark.read.option("mergeSchema", True).parquet(str(bronze_path))
    df_clean = df.fillna({"billing_amount": 0})
    age_mean_row = df_clean.select(mean(col("age")).alias("m")).collect()[0]["m"]
    if age_mean_row is not None:
        df_clean = df_clean.fillna({"age": age_mean_row})
    df_clean = df_clean.dropDuplicates(["patient_id"])
    df_clean.write.mode("overwrite").partitionBy("visit_date").parquet(str(silver_path))
