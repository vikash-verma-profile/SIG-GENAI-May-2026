from pathlib import Path

import pytest

pytest.importorskip("pyspark")

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, sum as spark_sum


LAB_ROOT = Path(__file__).resolve().parent.parent


def test_bangalore_total_revenue_matches_expected():
    spark = SparkSession.builder.master("local[1]").appName("lab7-test").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    try:
        rides = spark.read.option("header", True).option("inferSchema", True).csv(
            str(LAB_ROOT / "data" / "rides.csv")
        )
        drivers = spark.read.option("header", True).option("inferSchema", True).csv(
            str(LAB_ROOT / "data" / "drivers.csv")
        )

        rides_filtered = rides.filter(rides.city == "Bangalore")
        joined = rides_filtered.join(broadcast(drivers), "driver_id")
        revenue = joined.groupBy("city").agg(spark_sum("fare").alias("total_revenue"))

        row = revenue.collect()[0].asDict()
        assert row["city"] == "Bangalore"
        assert int(row["total_revenue"]) == 350
    finally:
        spark.stop()
