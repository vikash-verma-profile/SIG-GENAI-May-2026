"""PySpark optional: union CSV inputs with evolving schemas."""
from pathlib import Path

from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parent


def main() -> None:
    spark = SparkSession.builder.appName("SchemaEvolution").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    paths = [
        ROOT / "data" / "products_day1.csv",
        ROOT / "data" / "products_day2.csv",
        ROOT / "data" / "products_day3.csv",
    ]
    dfs = [
        spark.read.option("header", True).option("inferSchema", True).csv(str(p)) for p in paths
    ]
    merged = dfs[0]
    for nxt in dfs[1:]:
        merged = merged.unionByName(nxt, allowMissingColumns=True)

    merged.printSchema()
    merged.show()
    spark.stop()


if __name__ == "__main__":
    main()
