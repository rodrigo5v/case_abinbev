from delta import *
from pyspark.sql import SparkSession

builder = SparkSession.builder\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .appName("Gold layer")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sparkContext.setLogLevel("INFO")

storage_source = f"/home/rods/storage/silver/"
storage_target = f"/home/rods/storage/gold/"

df = spark.read.format("delta").load(storage_source)
df_agg = df.groupBy('country', 'state_province', 'brewery_type').count().withColumnRenamed("count","quantidade")

df_agg.write.mode('overwrite').format("delta").save(storage_target)