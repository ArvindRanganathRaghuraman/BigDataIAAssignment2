from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Ensure the scripts directory is included in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

# Import the function after updating the path
from download_sec_data import extract_and_upload_to_s3

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'catchup': False,  
}


# Define Airflow DAG
with DAG(
    dag_id="sec_data_extraction_dag",
    start_date=datetime(2025, 2, 8),
    schedule_interval="@daily",  
    catchup=False
) as dag:

    extract_and_upload_task = PythonOperator(
        task_id="extract_and_upload_to_s3",
        python_callable=extract_and_upload_to_s3
    )

    extract_and_upload_task
