from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.dates import days_ago

tables = ["ORDERS", "CUSTOMERS", "PAYMENTS"]

with DAG(
    dag_id="snowflake_dynamic_processing",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    for table in tables:
        SnowflakeOperator(
            task_id=f"transform_{table.lower()}",
            snowflake_conn_id="snowflake_default",
            sql=f"""
                INSERT INTO ANALYTICS.STG_{table}
                SELECT * FROM SOURCE_DB.PUBLIC.{table};
            """
        )