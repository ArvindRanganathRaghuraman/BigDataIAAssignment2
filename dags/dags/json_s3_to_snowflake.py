import pendulum
from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator  # Using EmptyOperator instead of DummyOperator


json_stage = "JSON_S3_STAGE"
target_quarters = ["2024q1json", "2024q2json", "2024q3json", "2024q4json"]


quarter_table_mapping = {
    "2024q1json": "Q1",
    "2024q2json": "Q2",
    "2024q3json": "Q3",
    "2024q4json": "Q4",
}


default_args = {
    'owner': 'findata',
    'start_date': pendulum.today('UTC').add(days=-1),  
}


dag = DAG(
    dag_id='load_json_stage_to_snowflake',
    default_args=default_args,
    schedule="@daily",
    catchup=False,
)


start = EmptyOperator(task_id="start", dag=dag)


def list_json_files(**kwargs):
    quarter = kwargs["quarter"]
    ti = kwargs["ti"]
    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    
    sql = f"LIST @{json_stage}/{quarter}/"
    results = hook.get_records(sql)
    
    json_files = []
    for row in results:
        file_path = row[0]  # ✅ Ensure this is the correct path
        file_name = file_path.split("/")[-1]
        if file_name.endswith(".json"):
            json_files.append(file_name)

    
    print(f"Files found in Snowflake stage for {quarter}: {json_files}")

    if not json_files:
        print(f"⚠️ No JSON files found in {json_stage}/{quarter}/")

    
    ti.xcom_push(key=f"json_files_{quarter}", value=json_files)


def load_json_from_stage(**kwargs):
    ti = kwargs["ti"]
    quarter = kwargs["quarter"]
    
    
    json_files = ti.xcom_pull(task_ids=f"list_json_{quarter}", key=f"json_files_{quarter}")

    if not json_files:
        print(f"⚠️ No JSON files to load for {quarter}")
        return  

    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    target_table = quarter_table_mapping.get(quarter)

    if not target_table:
        print(f"❌ ERROR: No mapping found for quarter: {quarter}")
        return  

    for json_file in json_files:
        file_path = f"{quarter}/{json_file}"

        sql = f"""
            COPY INTO {target_table} (FILE_NAME, JSON_CONTENT, UPLOADED_AT)  
            FROM (
                SELECT '{json_file}', $1, CURRENT_TIMESTAMP 
                FROM @{json_stage}/{file_path}
            )  
            FILE_FORMAT = (TYPE = JSON)
            FORCE = TRUE;
        """
        
        
        print(f"Running COPY INTO for {json_file} into {target_table}")
        
        hook.run(sql)


json_tasks = []
for quarter in target_quarters:
    list_task = PythonOperator(
        task_id=f"list_json_{quarter}",
        python_callable=list_json_files,
        op_kwargs={"quarter": quarter},
        
        dag=dag,
    )

    load_task = PythonOperator(
        task_id=f"load_json_{quarter}",
        python_callable=load_json_from_stage,
        op_kwargs={"quarter": quarter},
        
        dag=dag,
    )

    list_task >> load_task  
    json_tasks.append(load_task)


end = EmptyOperator(task_id="end", dag=dag)


start >> json_tasks >> end
