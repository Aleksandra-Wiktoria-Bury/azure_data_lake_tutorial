# Databricks notebook source
df = spark.read.option("inferSchema", True).option("header", True).csv("/mnt/raw_data/mock_data.csv")

# COMMAND ----------

# dbutils.fs.ls("/mnt")

# COMMAND ----------

df.write.parquet("/mnt/transform_data/mock.parquet")

