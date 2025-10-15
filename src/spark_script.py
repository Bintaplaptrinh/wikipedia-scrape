from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, sum as spark_sum, avg, count, desc
import os
import dotenv

dotenv.load_dotenv()
HDFS_PATH = os.getenv(f"HDFS_PATH")

spark = SparkSession.builder.appName("wikiAnalyst").getOrCreate()

df = spark.read.json(HDFS_PATH)

#q1: tong dan so/region
q1 = df.groupBy("Region").agg(spark_sum("population").alias("total_population"))
q1.show()

#q2: top 10 density (filter area_km2 > 0)
q2 = (
    df.filter(col("area_km2") > 0)
    .orderBy(desc("density"))
    .select("Country", "Region", "density", "population", "area_km2")
    .limit(10)
)
q2.show()


#q3: phân phối pop_bucket: pop_bucket/t1
q3 = (
    df.groupBy("pop_bucket")
    .agg(count("*").alias("count"))
)
q3.orderBy("pop_bucket").show()

spark.stop()