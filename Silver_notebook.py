# Databricks notebook source
from pyspark.sql.functions import lit, current_timestamp
import uuid

run_id = str(uuid.uuid4())
git_commit = "v1"
job_name = "demo_silver_pipeline"

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

# Get Bronze version
history = spark.sql("DESCRIBE HISTORY bronze_orders")
input_version = history.select("version").first()[0]

# Transform data
df = spark.read.table("bronze_orders") \
    .filter("status = 'completed' AND amount > 12000")

df_out = df \
    .withColumn("run_id", lit(run_id)) \
    .withColumn("processed_at", current_timestamp())

# Write Silver table
spark.sql("DROP TABLE IF EXISTS silver_orders")

df_out.write.format("delta") \
      .mode("overwrite") \
      .saveAsTable("silver_orders")

# Capture Silver version
silver_version = spark.sql("DESCRIBE HISTORY silver_orders") \
                     .select("version") \
                     .first()[0]

# Log dataset versions
spark.sql(f"""
INSERT INTO dataset_versions VALUES (
 'silver_orders',
 '{silver_version}',
 '{run_id}',
 current_timestamp()
)
""")

spark.sql(f"""
INSERT INTO dataset_versions VALUES (
 'bronze_orders',
 '{input_version}',
 '{run_id}',
 current_timestamp()
)
""")

# Log lineage
spark.sql(f"""
INSERT INTO lineage_edges VALUES (
 'silver_orders',
 'bronze_orders',
 '{input_version}',
 '{run_id}'
)
""")