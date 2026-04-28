%sql
SELECT * FROM pipeline_runs;
SELECT * FROM dataset_versions;
SELECT * FROM lineage_edges;


SELECT
    dv.table_name AS dataset,
    dv.version AS dataset_version,
    le.input_table AS depends_on,
    le.input_version AS input_version_used,
    pr.git_commit AS code_version,
    pr.start_time AS run_time
FROM dataset_versions dv
JOIN pipeline_runs pr
    ON dv.run_id = pr.run_id
LEFT JOIN lineage_edges le
    ON dv.run_id = le.run_id
ORDER BY pr.start_time DESC;
