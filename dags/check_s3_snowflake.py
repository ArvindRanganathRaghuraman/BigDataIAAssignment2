from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from datetime import datetime


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 8),
    'retries': 0
}


dag = DAG(
    dag_id='check_s3_snowflake_connection',
    default_args=default_args,
    schedule_interval=None,  
    catchup=False
)

def check_s3_connection():
    s3hook=S3Hook(aws_conn_id='aws_default')
    s3_client=s3hook.get_conn()
    buckets=s3_client.list_buckets()
    if buckets:
        print("s3 connection successfull")
    else:
        print("try again")

def check_snowflake_connection():
    snowflake_hook=SnowflakeHook(snowflake_conn_id='snowflake_default')
    conn=snowflake_hook.get_conn()
    cursor=conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    version=cursor.fetchone()
    print("snowflake connection successful,version:",version[0])

#defining the airflow tasks
check_s3_task=PythonOperator(
        task_id='check_s3_connection',
        python_callable=check_s3_connection,
        dag=dag
    )

chech_snowflake_task=PythonOperator(
        task_id='check_snowflake_connection',
        python_callable=check_snowflake_connection,
        dag=dag
    )

#define task dependencies
check_s3_task >> chech_snowflake_task
