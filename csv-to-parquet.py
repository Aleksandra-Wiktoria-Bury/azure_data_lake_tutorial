# Databricks notebook source
from pyspark.sql.functions import current_timestamp

# COMMAND ----------

dbutils.widgets.text("raw_path", "","")
dbutils.widgets.text("transform_path", "","")
transform_path = dbutils.widgets.get("transform_path")
raw_path = dbutils.widgets.get("raw_path")

# COMMAND ----------

df = spark.read.option("inferSchema", True).option("header", True).csv(raw_path)

# COMMAND ----------

# saves df to parquet with a timestamp col
df.withColumn("timestamp", current_timestamp()).write.mode("overwrite").parquet(transform_path)


# COMMAND ----------

df.display()

# COMMAND ----------


