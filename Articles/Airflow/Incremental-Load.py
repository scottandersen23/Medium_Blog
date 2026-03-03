from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import datetime

def incremental_load(**context):
    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")

    watermark_query = """
        SELECT COALESCE(MAX(UPDATED_AT), '1970-01-01')
        FROM ANALYTICS.RAW_ORDERS;
    """

    last_watermark = hook.get_first(watermark_query)[0]

    load_query = f"""
        INSERT INTO ANALYTICS.RAW_ORDERS
        SELECT *
        FROM SOURCE_DB.PUBLIC.ORDERS
        WHERE UPDATED_AT > '{last_watermark}';
    """

    hook.run(load_query)

with DAG(
    dag_id="snowflake_incremental_ingestion",
    start_date=days_ago(1),
    schedule_interval="@hourly",
    catchup=False
) as dag:

    load_incremental = PythonOperator(
        task_id="incremental_load_orders",
        python_callable=incremental_load
    )