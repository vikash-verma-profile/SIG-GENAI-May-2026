"""Ride-sharing analytics with broadcast join + partitioning."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, sum as spark_sum

ROOT = Path(__file__).resolve().parent


def main() -> None:
    spark = SparkSession.builder.appName("RideAnalytics").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    rides = spark.read.option("header", True).option("inferSchema", True).csv(str(ROOT / "data" / "rides.csv"))
    drivers = spark.read.option("header", True).option("inferSchema", True).csv(str(ROOT / "data" / "drivers.csv"))

    rides = rides.repartition(4)
    rides_filtered = rides.filter(rides.city == "Bangalore")
    optimized_df = rides_filtered.join(broadcast(drivers), "driver_id")

    revenue = optimized_df.groupBy("city").agg(spark_sum("fare").alias("total_revenue"))

    out_dir = ROOT / "output" / "partitioned_final"
    revenue.write.mode("overwrite").partitionBy("city").parquet(str(out_dir))
    revenue.show()

    spark.stop()


if __name__ == "__main__":
    main()
