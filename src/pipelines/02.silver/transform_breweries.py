from delta import *
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, StringType

builder = SparkSession.builder\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .appName("Silver layer")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sparkContext.setLogLevel("INFO")

date = datetime.now().date()
storage_source = f"/home/rods/storage/bronze/inserted_at={date}/*"
storage_target = f"/home/rods/storage/silver/"

schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("brewery_type", StringType(), True),
    StructField("address_1", StringType(), True),
    StructField("address_2", StringType(), True),
    StructField("address_3", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state_province", StringType(), True),
    StructField("postal_code", StringType(), True),
    StructField("country", StringType(), True),
    StructField("longitude", StringType(), True),
    StructField("latitude", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("website_url", StringType(), True),
    StructField("state", StringType(), True),
    StructField("street", StringType(), True)
])

df = spark.read.option('multiline', True).json(storage_source, schema=schema)

df = df.withColumn('latitude', col('latitude').cast('double'))
df = df.withColumn('longitude', col('longitude').cast('double'))
df = df.withColumn('inserted_at', lit(date))

df.show()

df.write.mode('overwrite').option('overwriteSchema', True).format("delta").partitionBy("country", "state_province").save(storage_target)