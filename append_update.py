# Databricks notebook source
from pyspark.sql.functions import current_timestamp
spark.conf.set('spark.sql.session.timeZone', 'CET')

# COMMAND ----------

dbutils.widgets.text("raw_path", "","")
dbutils.widgets.text("transform_path", "","")
dbutils.widgets.text("serving_path", "","")
dbutils.widgets.text("primary_key", "","")
primary_key = dbutils.widgets.get("primary_key")
raw_path = dbutils.widgets.get("raw_path")
transform_path = dbutils.widgets.get("transform_path")
serving_path = dbutils.widgets.get("serving_path")

# COMMAND ----------

df_tr = spark.read.parquet(transform_path)
df_raw = spark.read.option("inferSchema", True).option("header", True).csv(raw_path)

# COMMAND ----------

df_tr.display()
df_raw.display()

# COMMAND ----------

# creates a single-column df with duplicate rows
key_dupl = df_raw.join(df_tr, primary_key, 'inner').select(primary_key)

# COMMAND ----------

# Transform DF records that are not updated:
df_tr_dist = df_tr.join(key_dupl, primary_key, 'anti')
df_tr_dist.display()

# Raw DF records that are not updated:
df_raw_dist = df_raw.join(key_dupl, primary_key, 'anti')
df_raw_dist.display()

# COMMAND ----------

# Duplicate rows w/ records - middle step
reduced_df_tr = df_tr.join(key_dupl, primary_key)

reduced_df_raw = df_raw.join(key_dupl, primary_key)


# COMMAND ----------

cols = [primary_key, "first_name", "last_name", "email", "gender", "department", "active", "active_since", "IBAN", "credit_card", "pending_amount"]

# Duplicates but not changed
df_dupl = reduced_df_tr.join(reduced_df_raw, cols, "inner").select(cols)
df_dupl.display()

# Duplicates w/ updated records
df_dupl_upd = reduced_df_raw.join(reduced_df_tr, cols, "anti")

df_dupl_upd.display()

# COMMAND ----------

# Union and overwrite transform df w/ new timestamp

df_tr_dist.union(df_dupl.union(df_dupl_upd.union(df_raw_dist)).withColumn("timestamp", current_timestamp())).write.mode("overwrite").parquet(transform_path)

# COMMAND ----------

df = spark.read.parquet(transform_path).orderBy(primary_key)
df.display()

# COMMAND ----------

# DBTITLE 1,transform to serving
df.write.mode("overwrite").parquet(serving_path)
