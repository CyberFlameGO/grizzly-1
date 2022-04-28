# Scope File
Scope files provide instructions to Grizzly on when to generate your BigQuery Tables. The files are written in YAML and are named "SCOPE.yml".

| Field name | Notes |
|------------|-------|
| **schedule_interval** | Required. [YAML Scalar](https://www.javatpoint.com/yaml-scalars). <br><br> This field defines how often this job should run. The value is written using the CRON format. |
| **execution_timeout_per_table** | Required. [YAML Scalar](https://www.javatpoint.com/yaml-scalars).
| **etl_scope** | Required. [YAML Sequence](https://www.javatpoint.com/yaml-sequence). <br><br> Defines the active jobs that should be part of the Cloud Composer DAG. Values should be "[target_dataset].[target_view]” (without the quotes.)

