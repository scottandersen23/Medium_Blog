
# Airflow + Snowflake + dbt Production Demo

## Overview
This project demonstrates:

- Airflow orchestration
- Snowflake warehouse integration
- dbt transformations (staging + marts)
- Production DAG configuration

## Run Instructions

1. Configure dbt_project/profiles.yml with Snowflake credentials.
2. Start Airflow:
   docker-compose -f docker/docker-compose.yml up
3. Access Airflow UI at http://localhost:8080
4. Trigger DAG: snowflake_dbt_ingestion_pipeline
