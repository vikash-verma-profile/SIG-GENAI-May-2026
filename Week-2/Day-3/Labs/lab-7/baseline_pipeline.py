"""Unoptimized baseline join for comparison (lab exercise)."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum

ROOT = Path(__file__).resolve().parent


def main() -> None:
    spark = SparkSession.builder.appName("RideAnalyticsBaseline").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    rides = spark.read.option("header", True).option("inferSchema", True).csv(str(ROOT / "data" / "rides.csv"))
    drivers = spark.read.option("header", True).option("inferSchema", True).csv(str(ROOT / "data" / "drivers.csv"))

    joined_df = rides.join(drivers, "driver_id")
    revenue = joined_df.groupBy("city").agg(spark_sum("fare").alias("total_revenue"))
    revenue.write.mode("overwrite").parquet(str(ROOT / "output" / "baseline"))
    revenue.show()
    spark.stop()


if __name__ == "__main__":
    main()
