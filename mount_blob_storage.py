# Databricks notebook source
# Mount data lake storage:

config = {"fs.azure.account.key.aleksdatalake.blob.core.windows.net":dbutils.secrets.get(scope = "adf-tutorial-secret-scope", key = "adf-tutorial-dbks")}

dbutils.fs.mount(
source = "wasbs://raw@aleksdatalake.blob.core.windows.net",
mount_point = "/mnt/raw_data",
extra_configs = config )

dbutils.fs.mount(
source = "wasbs://transform@aleksdatalake.blob.core.windows.net",
mount_point = "/mnt/transform_data",
extra_configs = config)

dbutils.fs.mount(
source = "wasbs://serving@aleksdatalake.blob.core.windows.net",
mount_point = "/mnt/serving_data",
extra_configs = config)

# COMMAND ----------

'''pwd = dbutils.secrets.get(scope = "adf-tutorial-secret-scope", key = "adf-tutorial-dbks")
print(pwd)'''
