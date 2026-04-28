📘 Foundry-Style Lineage Implementation in Databricks (Without dbt)
📌 Project Overview

This project demonstrates how to implement Palantir Foundry–style data lineage, versioning, and reproducibility in Databricks using Delta Lake, without using dbt.

Instead of automatic lineage tools, this project builds:

Explicit lineage tracking
Dataset version tracking
Pipeline execution tracking
Code traceability

using custom metadata tables.

🧠 Core Objective

Every dataset must answer:

✅ Which code created it?
✅ Which input data version was used?
✅ Which pipeline run produced it?

This project ensures full traceability across:

Data  →  Code  →  Pipeline Execution
🏗 Architecture
Source Data
     ↓
Bronze Layer (Raw Ingestion)
     ↓
Silver Layer (Transformations)
     ↓
Custom Metadata Tracking
📂 Repository Structure
foundry-style-databricks-lineage/
│
├── 01_bronze_layer.py
├── 02_silver_layer.py
├── metadata_tables.sql
├── recruiter_audit_view.sql
└── README.md
⚙️ Technologies Used
Databricks
Delta Lake
PySpark
SQL
Git (for code version tracking)
🧱 Metadata Framework (Custom Replacement for dbt)

This project creates 3 core metadata tables:

1️⃣ pipeline_runs

Tracks every pipeline execution.

Column	Description
run_id	Unique pipeline execution ID
job_name	Name of pipeline (bronze/silver)
git_commit	Code version identifier
start_time	Execution timestamp
status	SUCCESS / FAILED
2️⃣ dataset_versions

Tracks Delta table versions used in each run.

Column	Description
table_name	Dataset name
version	Delta version number
run_id	Associated pipeline run
created_at	Timestamp
3️⃣ lineage_edges

Tracks dataset dependencies.

Column	Description
output_table	Produced dataset
input_table	Source dataset
input_version	Delta version used
run_id	Pipeline run ID
🔄 End-to-End Flow
🥉 Bronze Layer
Creates sample dataset
Stores it as Delta table (bronze_orders)
Logs pipeline run
🥈 Silver Layer
Reads Bronze table
Filters completed orders
Adds metadata columns:
run_id
git_commit
processed_at
Writes to silver_orders
Captures:
Input Delta version
Output Delta version
Lineage relationship
🔍 Reproducibility Example

If revenue drops unexpectedly:

Query dataset_versions
Identify run_id
Check pipeline_runs for git_commit
Check lineage_edges for input version

You can:

Re-run the pipeline
Compare Delta versions
Audit the exact code version used
🧪 Recruiter Audit View

The project includes recruiter_audit_view.sql, which joins:

pipeline_runs
dataset_versions
lineage_edges

to produce a single traceability view.

This demonstrates Foundry-style auditability without dbt.

🚀 Key Features

✔ Explicit lineage tracking
✔ Delta version-based reproducibility
✔ Code-to-data traceability
✔ Metadata-driven auditing
✔ Clean Bronze → Silver architecture

📌 What This Project Demonstrates

Even without dbt or Foundry, it is possible to build:

Enterprise-grade data traceability
Version-controlled transformations
Reproducible pipelines
Dependency tracking

using Databricks + Delta Lake + disciplined metadata design.

🎯Summary

“This project implements Foundry-style auditing in Databricks by capturing run IDs, Git commit versions, and Delta table versions during each pipeline execution, and storing lineage relationships in custom metadata tables. This enables full traceability and reproducibility across data, code, and pipelines without using dbt.”

👨‍💻 Author

Tharun Vallabhu
Databricks | Data Engineering | Delta Lake | Metadata-driven pipelines
