from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
import pandas as pd
import io

s3_bucket = "s3-airflow-bucket-1"
s3_prefix = "ceac_financial_statements/2024q4/"
expected_files = ["sub.txt", "pre.txt", "tag.txt", "num.txt"]

required_columns = {
    "sub.txt": ["adsh", "cik", "name", "sic", "countryba", "stprba", "cityba", "zipba", "form", "period", "filed", "accepted"],
    "pre.txt": ["adsh", "report", "line", "stmt", "rfile", "tag", "version", "plabel", "negating"],
    "tag.txt": ["tag", "version", "custom", "abstract", "datatype", "iord", "crdr", "tlabel", "doc"],
    "num.txt": ["adsh", "tag", "version", "ddate", "qtrs", "uom", "segments", "coreg", "value", "footnote"]
}



default_args = {
    'owner': 'findata',
    'start_date': days_ago(1),
}

dag = DAG(
    'validate_data_stage',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)


start = DummyOperator(task_id="start", dag=dag)

#listing the files first
def list_s3_files():
    hook = S3Hook(aws_conn_id="aws_default")
    files = hook.list_keys(bucket_name=s3_bucket, prefix=s3_prefix)
    
    if files:
        print(f"Files found in {s3_prefix}: {files}")
    else:
        raise ValueError(f" No files found in {s3_prefix}")

#check if files exist
def check_files_exist():
    hook = S3Hook(aws_conn_id="aws_default")
    available_files = hook.list_keys(bucket_name=s3_bucket, prefix=s3_prefix)

    if not available_files:
        raise ValueError(f"No files found in {s3_prefix}")

    missing_files = [file for file in expected_files if f"{s3_prefix}{file}" not in available_files]

    if missing_files:
        raise ValueError(f"Missing files in S3: {', '.join(missing_files)}")
    
    print(f"All required files are present: {expected_files}")

#validating the file structure
def validate_csv_file(file_name):
    hook = S3Hook(aws_conn_id="aws_default")
    file_path = f"{s3_prefix}{file_name}"
    
    # Read file from S3
    file_obj = hook.get_key(file_path, bucket_name=s3_bucket)
    file_content = file_obj.get()["Body"].read().decode("utf-8")
    
    # Load CSV into Pandas
    df = pd.read_csv(io.StringIO(file_content), delimiter="\t")  # Assuming tab-delimited

   #checking the columns
    missing_cols = [col for col in required_columns[file_name] if col not in df.columns]
    if missing_cols:
        raise ValueError(f"File {file_name} is missing required columns: {', '.join(missing_cols)}")


    if df.empty:
        raise ValueError(f"File {file_name} is empty!")

  
    print(f"Validation Passed: {file_name} contains {len(df)} records.")

#defining tasks 
list_s3_task = PythonOperator(
    task_id="list_s3_files",
    python_callable=list_s3_files,
    dag=dag,
)

check_s3_files = PythonOperator(
    task_id="check_s3_files",
    python_callable=check_files_exist,
    dag=dag,
)

validate_sub = PythonOperator(
    task_id="validate_sub",
    python_callable=validate_csv_file,
    op_args=["sub.txt"],
    dag=dag,
    trigger_rule="all_done",  
)

validate_pre = PythonOperator(
    task_id="validate_pre",
    python_callable=validate_csv_file,
    op_args=["pre.txt"],
    dag=dag,
    trigger_rule="all_done",
)

validate_tag = PythonOperator(
    task_id="validate_tag",
    python_callable=validate_csv_file,
    op_args=["tag.txt"],
    dag=dag,
    trigger_rule="all_done",
)

validate_num = PythonOperator(
    task_id="validate_num",
    python_callable=validate_csv_file,
    op_args=["num.txt"],
    dag=dag,
    trigger_rule="all_done",
)


end = DummyOperator(task_id="end", dag=dag)

#tasks execution
start >> list_s3_task >> check_s3_files
check_s3_files >> [validate_sub, validate_pre, validate_tag, validate_num] >> end
