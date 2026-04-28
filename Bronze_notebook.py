# Databricks notebook source
import uuid
from pyspark.sql.functions import current_timestamp

# Create run info
run_id = str(uuid.uuid4())
git_commit = "v1"
job_name = "demo_bronze_pipeline"

print("Run ID:", run_id)

# Log pipeline run
spark.sql(f"""
INSERT INTO pipeline_runs VALUES (
 '{run_id}',
 '{job_name}',
 '{git_commit}',
 current_timestamp(),
 'SUCCESS'
)
""")

# Create sample data
data = [
    (1, "completed", 10000),
    (2, "pending", 5000),
    (3, "completed", 20000),
    (4, "completed", 15000)
]

df = spark.createDataFrame(data, ["order_id", "status", "amount"]) \
          .withColumn("ingested_at", current_timestamp())

# Write Bronze table
spark.sql("DROP TABLE IF EXISTS bronze_orders")

df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("bronze_orders")

# Capture Bronze version
bronze_version = spark.sql("DESCRIBE HISTORY bronze_orders") \
                      .select("version") \
                      .first()[0]

# Log dataset version
spark.sql(f"""
INSERT INTO dataset_versions VALUES (
 'bronze_orders',
 '{bronze_version}',
 '{run_id}',
 current_timestamp()
)
""")