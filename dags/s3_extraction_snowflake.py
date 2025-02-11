from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

# S3 and Snowflake Configurations
s3_bucket = "s3-airflow-bucket-1"
s3_prefix = "ceac_financial_statements/2024q4/"
snowflake_stage = "my_s3_stage"

# DAG Default Arguments
default_args = {
    'owner': 'findata',
    'start_date': days_ago(1),
}

# DAG Definition
dag = DAG(
    'extract_data_stage',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

# Dummy Start Task
start = DummyOperator(task_id="start", dag=dag)

# Function to load data into Snowflake using SnowflakeHook
def load_data_into_snowflake(file_name: str, table_name: str):
    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    sql = f"""
        COPY INTO {table_name}
        FROM @my_s3_stage/2024q4/{file_name}
        FILE_FORMAT = my_csv_format
        FORCE = TRUE;
    """
    hook.run(sql)

# Create PythonOperator tasks for sub.txt, pre.txt, and tag.txt
load_sub = PythonOperator(
    task_id="load_sub",
    python_callable=load_data_into_snowflake,
    op_args=["sub.txt", "RAW_SUB"],  # Pass file name and table name
    dag=dag,
)

load_pre = PythonOperator(
    task_id="load_pre",
    python_callable=load_data_into_snowflake,
    op_args=["pre.txt", "RAW_PRE"],  # Pass file name and table name
    dag=dag,
)

load_tag = PythonOperator(
    task_id="load_tag",
    python_callable=load_data_into_snowflake,
    op_args=["tag.txt", "RAW_TAG"],  # Pass file name and table name
    dag=dag,
)

# Dummy End Task
end = DummyOperator(task_id="end", dag=dag)

# Task Dependencies
start >> [load_sub, load_pre, load_tag] >> end
