import os
import logging
import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from botocore.exceptions import BotoCoreError, NoCredentialsError, EndpointConnectionError, ClientError
from botocore.config import Config
from dotenv import load_dotenv
from datetime import datetime
import time


load_dotenv(".env")  

AWS_ACCESS_KEY = os.getenv("ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("SECRET_ACCESS_KEY")
REGION = os.getenv("REGION")


s3_bucket_name = "s3-airflow-bucket-1"
s3_folder_name = "json-folder"  # Folder inside S3


data_folder = "/opt/airflow/data/Json_Data"


s3_config = Config(
    retries={'max_attempts': 5, 'mode': 'standard'},
    connect_timeout=120,
    read_timeout=120
)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 8),
    "retries": 1
}


def list_json_files(**kwargs):
    file_list = []
    
    if not os.path.exists(data_folder):
        logging.error(f"❌ Directory not found: {data_folder}")
        raise FileNotFoundError(f"Directory not found: {data_folder}")

    for quarter_folder in os.listdir(data_folder):  
        quarter_path = os.path.join(data_folder, quarter_folder)

        if os.path.isdir(quarter_path):  
            for root, _, files in os.walk(quarter_path):  
                for file in files:
                    if file.endswith(".json"):
                        local_path = os.path.join(root, file)
                        s3_key = os.path.relpath(local_path, data_folder)  
                        s3_key = f"{s3_folder_name}/{s3_key}"
                        file_list.append((local_path, s3_key))

    if not file_list:
        logging.warning("⚠ No JSON files found!")

    logging.info(f" Found {len(file_list)} JSON files.")
    kwargs['ti'].xcom_push(key='json_files', value=file_list)


def upload_json_files_to_s3(**kwargs):
    ti = kwargs['ti']
    json_files = ti.xcom_pull(task_ids='list_json_files', key='json_files')

    if not json_files:
        logging.info("⚠ No JSON files found. Skipping upload tasks.")
        return
    
    
    s3_hook = S3Hook(aws_conn_id="aws_default")
    s3_client = boto3.client('s3', config=s3_config)

    
    try:
        s3_hook.get_conn().put_object(Bucket=s3_bucket_name, Key=f"{s3_folder_name}/")
        logging.info(f"📁 Created new folder in S3: s3://{s3_bucket_name}/{s3_folder_name}/")
    except Exception as e:
        logging.warning(f"⚠ Failed to create folder in S3: {e}")

    
    for local_path, s3_key in json_files:
        try:
            with open(local_path, 'rb') as json_file:
                file_size = os.path.getsize(local_path)
                logging.info(f"📂 Uploading {local_path} ({file_size} bytes) to S3")

                if file_size > 10 * 1024 * 1024:  
                    multipart_upload_to_s3(s3_client, s3_bucket_name, s3_key, local_path)
                else:
                    retry_s3_upload(s3_hook, json_file.read(), s3_key, s3_bucket_name)
                
                logging.info(f" Uploaded {local_path} to s3://{s3_bucket_name}/{s3_key}")
        except (BotoCoreError, NoCredentialsError, EndpointConnectionError, ClientError) as e:
            logging.error(f"❌ Failed to upload {local_path}: {e}")


def retry_s3_upload(s3_hook, file_data, s3_key, bucket, retries=3):
    for attempt in range(1, retries + 1):
        try:
            s3_hook.load_bytes(file_data, key=s3_key, bucket_name=bucket, replace=True)
            return
        except Exception as e:
            logging.warning(f"⚠ Attempt {attempt}/{retries} failed for {s3_key}: {e}")
            time.sleep(2**attempt)  

    logging.error(f"❌ Failed to upload {s3_key} after {retries} attempts.")


def multipart_upload_to_s3(s3_client, bucket, s3_key, local_file_path):
    """ Upload large files to S3 using Multipart Upload """
    upload_id = None  
    try:
        logging.info(f"📦 Initiating Multipart Upload: {local_file_path}")
        multipart_upload = s3_client.create_multipart_upload(Bucket=bucket, Key=s3_key)
        upload_id = multipart_upload['UploadId']
        
        part_size = 10 * 1024 * 1024  
        parts = []
        with open(local_file_path, 'rb') as file:
            part_number = 1
            while True:
                data = file.read(part_size)
                if not data:
                    break

                part = s3_client.upload_part(
                    Bucket=bucket,
                    Key=s3_key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=data
                )
                parts.append({"PartNumber": part_number, "ETag": part['ETag']})
                logging.info(f" Uploaded Part {part_number} for {s3_key}")
                part_number += 1

       
        s3_client.complete_multipart_upload(
            Bucket=bucket,
            Key=s3_key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        logging.info(f"Successfully completed multipart upload for {s3_key}")

    except Exception as e:
        logging.error(f" Multipart Upload Failed for {s3_key}: {e}")
        if upload_id:
            s3_client.abort_multipart_upload(Bucket=bucket, Key=s3_key, UploadId=upload_id)


with DAG(
    dag_id="upload_json_to_s3_hook",
    default_args=default_args,
    schedule="@daily",
    catchup=False
) as dag:
    
    
    list_files_task = PythonOperator(
        task_id="list_json_files",
        python_callable=list_json_files,
        provide_context=True
    )

    
    upload_task = PythonOperator(
        task_id="upload_json_files_to_s3",
        python_callable=upload_json_files_to_s3,
        provide_context=True
    )

    
    list_files_task >> upload_task
