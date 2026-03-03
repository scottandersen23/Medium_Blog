from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="snowflake_merge_upsert",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    merge_orders = SnowflakeOperator(
        task_id="merge_into_staging",
        snowflake_conn_id="snowflake_default",
        sql="""
            MERGE INTO ANALYTICS.STG_ORDERS t
            USING ANALYTICS.RAW_ORDERS s
            ON t.ORDER_ID = s.ORDER_ID
            WHEN MATCHED THEN
                UPDATE SET t.ORDER_TOTAL = s.ORDER_TOTAL
            WHEN NOT MATCHED THEN
                INSERT (ORDER_ID, ORDER_TOTAL)
                VALUES (s.ORDER_ID, s.ORDER_TOTAL);
        """
    )