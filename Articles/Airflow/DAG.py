from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="snowflake_sql_execution",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["snowflake", "elt"]
) as dag:

    transform_sales = SnowflakeOperator(
        task_id="transform_sales_data",
        snowflake_conn_id="snowflake_default",
        sql="""
            INSERT INTO ANALYTICS.MART_DAILY_SALES
            SELECT
                ORDER_DATE,
                SUM(ORDER_TOTAL) AS TOTAL_REVENUE
            FROM ANALYTICS.STG_ORDERS
            GROUP BY ORDER_DATE;
        """
    )