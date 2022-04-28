# Developing Your Grizzly Data Warehouse
## (1) Build the Base Data Layer
### Import data from BigQuery
**(1) Give data access to the Data Source.**

Grizzly uses Composer to import data into BigQuery. You'll need to give "read" access to the data source to following accounts:
- DEV environment: [DEV Project ID]-compute@developer.gserviceaccount.com
- UAT environment: [UAT Project ID]-compute@developer.gserviceaccount.com
- PROD environment: [PROD Project ID]-compute@developer.gserviceaccount.com

You can find the name of the Composer account through [IAM settings](https://console.cloud.google.com/iam-admin/iam) in their respective projects.

**(2) Check out the DEV branch of the source code repository.**

**(3) Create a BigQuery Dataset for the data source system you are importing.**

The new dataset follows the naming convention "bas_[data_source]". Instructions for creating BigQuery datasets can be found in the [BigQuery documentation](https://cloud.google.com/bigquery/docs/datasets).

**(4) Create a new source code directory for the data source system you are importing.**

The directory should reside under the /base/ directory and match the name of the dataset you created in the previous step.

**(5) Create a [Scope File](./scope_file.md) named "SCOPE.yml" in the directory.**

**(6) Create a [Table Definition File](./table_definition_file.md) for each table that you'd like to add from your data source.**

 The file should be named "bas_[data_source].[table_name].yml".

**(7) Create the supporting queries to generate the table.**

In the [Table Definition File](./table_definition_file.md), the *stage_loading_query* field defines a SQL query file used to generate the table. These SQL query files live in a subdirectory of the base/bas_[data_source]/ directory called queries.

You may also define the *job_quality_data_check_query* field that will run a set of checks that you define at the conclusion of the tables generation. These SQL query files should also live in the queries subdirectory.

**(8) Repeat steps 6 and 7 to define any additional tables needed from the data source.**

**(9) Commit your code.**

**(10) Deploy the code using Build Triggers.**

### Import data from CloudSQL / Spanner

**(1) Give data access to the Data Source.**

This connectivity uses [BigQuery's Federated Queries](https://cloud.google.com/bigquery/docs/federated-queries-intro) feature.

If importing from CloudSQL, in the GCP project that contains the CloudSQL [source_table], [enable the BigQuery connection service](https://cloud.google.com/bigquery/docs/cloud-sql-federated-queries#enable_the_connection_service), [add public IP connectivity with no authorized address](https://cloud.google.com/bigquery/docs/cloud-sql-federated-queries#public_ip), and [set the CloudSQL database connection](https://cloud.google.com/bigquery/docs/cloud-sql-federated-queries#setting-up-cloud-sql-database-connections).

If importing from Spanner, in the GCP project that contains the Spanner [source_table], set the required [permissions](https://cloud.google.com/bigquery/docs/cloud-spanner-federated-queries#permissions), [enable the BigQuery connection service](https://cloud.google.com/bigquery/docs/cloud-spanner-federated-queries#enable_the_connection_service), and [set the Spanner database connection](https://cloud.google.com/bigquery/docs/cloud-spanner-federated-queries#setting-up-cloud-sql-database-connections).

**(2) Check out the DEV branch of the source code repository.**

**(3) Create a BigQuery Dataset for the data source system you are importing.**

The new dataset follows the naming convention "bas_[data_source]". Instructions for creating BigQuery datasets can be found in the [BigQuery documentation](https://cloud.google.com/bigquery/docs/datasets).

**(4) Create a new source code directory for the data source system you are importing.**

The directory should reside under the /base/ directory and match the name of the dataset you created in the previous step.

**(5) Create a [Scope File](./scope_file.md) named "SCOPE.yml" in the directory.**

**(6) Create a [Table Definition File](./table_definition_file.md) for each table that you'd like to add from your data source.**

The file should be named "bas_[data_source].[table_name].yml".

**(7) Create the supporting queries to generate the table.**

In the [Table Definition File](./table_definition_file.md), the *stage_loading_query* field defines a SQL query file used to generate the table. These SQL query files live in a subdirectory of the *base/bas_[data_source]/* directory called _queries_.

The query should include the EXTERNAL_QUERY statement. Do not include a CREATE VIEW statement. See [bas_taxi.vw_taxi_mysql.sql](https://source.cloud.google.com/grizzly-test-data/grizzly_framework/+/main:grizzly_example/base/bas_taxi/queries/bas_taxi.vw_taxi_mysql.sql) file for an example.

You may also define a *job_quality_data_check_query* field that will run a set of checks that you define at the conclusion of the tables generation. These SQL query files should also live in the _queries_ subdirectory.

**(8) Repeat steps 6 and 7 to define any additional tables needed from the data source.**

**(9) Commit your code.**

**(10) Deploy the code using Build Triggers.**

### Import data from Google Sheets

**(1) Give data access to the Data Source.**

Grizzly uses Composer to import Google Sheets data into BigQuery. Give "read" access to the Google Sheet you'd like to import to following accounts:

* DEV environment: _[DEV Project ID]-compute@developer.gserviceaccount.com_
* UAT environment: _[UAT Project ID]-compute@developer.gserviceaccount.com_
* PROD environment: _[PROD Project ID]-compute@developer.gserviceaccount.com_

You can find the name of the Composer account through [IAM settings](https://console.cloud.google.com/iam-admin/iam) in their respective projects.

**(2) Check out the DEV branch of the source code repository.**

**(3) Create a BigQuery Dataset for the data source system you are importing.**

The new dataset follows the naming convention "bas_[data_source]". Instructions for creating BigQuery datasets can be found in the [BigQuery documentation](https://cloud.google.com/bigquery/docs/datasets).

**(4) Create a new source code directory for the data source system you are importing.**

The directory should reside under the /base/ directory and match the name of the dataset you created in the previous step.

**(5) Create a [Scope File](./scope_file.md) named "SCOPE.yml" in the directory.**

**(6) Create a [Table Definition File](#heading=h.glofe8s5zayq) for each table that you'd like to add from your data source.**

The file should be named "bas_[data_source].[table_name].yml".

The fields _source_type_, _source_gsheet_id_, and _source_columns_ are used to instruct Grizzly on how read data from the spreadsheet.

**(7) Create the supporting queries to generate the table.**

In the [Table Definition File](./table_definition_file.md), the stage_loading_query field defines a SQL query file used to generate the table. These SQL query files live in a subdirectory of the **base/bas_[data_source]/** directory called _queries_.

You may also define a *job_quality_data_check_query* field that will run a set of checks that you define at the conclusion of the tables generation. These SQL query files should also live in the _queries_ subdirectory.

**(8) Repeat steps 6 and 7 to define any additional tables needed from the data source.**

**(9) Commit your code.**

**(10) Deploy the code using Build Triggers.**

## Build the Business and Presentation Data Layer

**(1) Check out the DEV branch of the source code repository.**

**(2) Create a BigQuery Dataset for the data source system you are importing.**

BigQuery datasets within the [Business Data Layer](./concepts.md#business-data-layer) follow the naming convention "biz_[domain_name]". BigQuery datasets within the [Presentation Data Layer](./concepts.md#presentation-data-layer) follow the naming convention "prs_[domain_name]". Instructions for creating BigQuery datasets can be found in the [BigQuery documentation](https://cloud.google.com/bigquery/docs/datasets).

**(3) Create a new source code directory for the data source system you are importing. **

Grizzly stores related Business Data Layer and Presentation Table Definitions in a folder based on the table's business and operation domain. The directory should reside under a domain directory and match the [domain_name] of the dataset you created in the previous step.

**(4) Create a [Scope File](./scope_file.md) named "SCOPE.yml" in the directory.**

**(5) Create a [Table Definition File](./table_definition_file.md) for each table that you'd like to add from your data source.**

The file should be named "[biz/prs]_[domain_name].[table_name].yml".

**(6) Create the supporting queries to generate the table.**

In the [Table Definition File](./table_definition_file.md), the *stage_loading_query* field defines a SQL query file used to generate the table. These SQL query files live in a subdirectory of the _[domain_name]/_ directory called _queries_.

You may also define a *job_quality_data_check_query* field that will run a set of checks that you define at the conclusion of the tables generation. These SQL query files should also live in the _queries_ subdirectory.

**(7) Repeat steps 5 and 6 to define any additional tables needed for your business or presentation logic.**

**(8) Commit your code.**

**(9) Deploy the code using Build Triggers.**

## Managing Your Grizzly Installation

### Promoting code from DEV to UAT
1. Select the *domain* that you would like to promote from the [Development environment](./concepts.md#environments) to the [UAT environment](./concepts.md#environments). Possible options include:
    - "bq" to promote custom BigQuery supporting functions.
    - "base/[source_system]" to promote a dataset from your [Base Data Layer](./concepts.md#base-data-layer)
    - the name of a defined business and operational domain from your [Business](./concepts.md#business-data-layer) and [Presentation Data Layer](./concepts.md#presentation-data-layer)
1. In your metadata project, run the following [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers) to deploy the code in the destination environment.
    1. Run *merge-codebase* to merge your code from the "dev" branch to the "uat" branch"
        - Set the *_TARGET_BRANCH* substitution variable to "uat".
        - Set the *_DOMAIN* substitution variable to the domain selected in step 1.
    2. Run *deploy-bigquery* to deploy BigQuery assets in the UAT environment.
        - Set *branch* to "uat".
        - Set the *_DOMAIN* substitution variable to domain selected in step 1.
        - Set the *_ENVIRONMENT* substitution variable to "uat".
    3. Run *deploy-composer* to deploy Composer pipelines for building your assets.
        - Set *branch* to "uat".
        - Set the *_DOMAIN* substitution variable to domain selected in step 1.
        - Set the *_ENVIRONMENT* substitution variable to "uat".
    4. (Optional) Run *deploy-datacatalog* to deploy datacatalog assets.
        - Set *branch* to "uat".
    5. (Optional) Run *deploy-dataflow-pubsub-inbound* to deploy pub/sub infrastructure.
        - Set *branch* to "uat".
        - Set the *_DOMAIN* substitution variable to domain selected in step 1.
    6. (Optional) Run *deploy-dlp-deindentify* and *deploy-dlp-inspect* to deploy Data Loss Prevention functionality.
        - Set *branch* to "uat".
    7. (Optional) Run *deploy-policytag-taxonomy* to deploy Data Catalog policy tag.
        - Set *branch* to "uat"
1. Share your [Presentation Data Layer](./concepts.md#presentation-data-layer) with your testing user groups.
1. Your testing user groups will perform User Acceptance Testing to identify any issues with the data assets and determine if they are ready to deploy into the [Production Environment](./concepts.md#environments).

### Promoting code from UAT to PROD
1. Select the *domain* that you would like to promote from the [UAT environment](./concepts.md#environments) to the [Production environment](./concepts.md#environments). Possible options include:
    - "bq" to promote custom BigQuery supporting functions.
    - "base/[source_system]" to promote a dataset from your [Base Data Layer](./concepts.md#base-data-layer)
    - the name of a defined business and operational domain from your [Business](./concepts.md#business-data-layer) and [Presentation Data Layer](./concepts.md#presentation-data-layer)
1. In your metadata project, run the following [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers) to deploy the code in the destination environment.
    1. Run *merge-codebase* to merge your code from the "uat" branch to the "prod" branch"
        - Set the *_TARGET_BRANCH* substitution variable to "prod".
        - Set the *_DOMAIN* substitution variable to the domain selected in step 1.
    2. Run *deploy-bigquery* to deploy BigQuery assets in the UAT environment.
        - Set *branch* to "prod".
        - Set the *_DOMAIN* substitution variable to domain selected in step 1.
        - Set the *_ENVIRONMENT* substitution variable to "prod".
    3. Run *deploy-composer* to deploy Composer pipelines for building your assets.
        - Set *branch* to "prod".
        - Set the *_DOMAIN* substitution variable to domain selected in step 1.
        - Set the *_ENVIRONMENT* substitution variable to "prod".
    4. (Optional) Run *deploy-datacatalog* to deploy datacatalog assets.
        - Set *branch* to "prod".
    5. (Optional) Run *deploy-dataflow-pubsub-inbound* to deploy pub/sub infrastructure.
        - Set *branch* to "prod".
        - Set the *_DOMAIN* substitution variable to domain selected in step 1.
    6. (Optional) Run *deploy-dlp-deindentify* and *deploy-dlp-inspect* to deploy Data Loss Prevention functionality.
        - Set *branch* to "prod".
    7. (Optional) Run *deploy-policytag-taxonomy* to deploy Data Catalog policy tag.
        - Set *branch* to "prod"
1. Share your [Presentation Data Layer](./concepts.md#presentation-data-layer) with your user groups.

### Retire Jobs
* If a job is being retired, move the related .yml and .sql files to the **[project_root]/dev/base/[target_domain]/deprecated/** directory.
* If the entire [target_domain] is being retired, also move the SCOPE.yml file to the same deprecated directory. The retired DAG should be deleted from the Development, UAT, and Production Cloud Storage buckets.
* The movement of these retired files should be part of a Change List and promoted and deployed into the UAT and Production environments as part of the standard code promotion process. This step will remove any of the retired code that has been deployed in the UAT and Production environments.