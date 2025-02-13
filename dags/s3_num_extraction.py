from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago


s3_bucket = "s3-airflow-bucket-1"
s3_prefix = "ceac_financial_statements/2024q4/"
snowflake_stage = "my_s3_stage"

default_args = {
    'owner': 'findata',
    'start_date': days_ago(1),
}

# dag
dag = DAG(
    'extract_data_stage_1',
    default_args=default_args,  
    schedule_interval=None,
    catchup=False,
)

# Dummy Start Task
start = DummyOperator(task_id="start", dag=dag)

# funcrion to connect to snowflake
def load_data_into_snowflake_num():
    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    
    sql = f"""
        COPY INTO RAW_NUM
        FROM @my_s3_stage/2024q4/num.txt
        FILE_FORMAT = my_csv_format_num
        FORCE = TRUE;
    """
    hook.run(sql)


load_num = PythonOperator(
    task_id="load_num",
    python_callable=load_data_into_snowflake_num,
    dag=dag,
)


end = DummyOperator(task_id="end", dag=dag)

# tasks
start >> load_num >> end
