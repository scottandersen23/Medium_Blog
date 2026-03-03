from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="snowflake_copy_into_s3",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    copy_into_raw = SnowflakeOperator(
        task_id="copy_s3_to_raw",
        snowflake_conn_id="snowflake_default",
        sql="""
            COPY INTO ANALYTICS.RAW_ORDERS
            FROM @MY_S3_STAGE/orders/
            FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"')
            ON_ERROR = 'ABORT_STATEMENT';
        """
    )