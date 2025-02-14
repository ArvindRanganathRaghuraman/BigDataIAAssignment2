from diagrams import Diagram
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import S3
from diagrams.saas.analytics import Snowflake
from diagrams.custom import Custom

with Diagram("Data Pipeline",show=False):
    raw_storage = Custom("Raw Data","raw_data.jpg")
    airflow_pipeline = Airflow("Airflow")
    s3_bucket = S3("S3 Bucket")
    snowflake_storage = Snowflake("Snowflake")

    raw_storage >> airflow_pipeline >> s3_bucket >> snowflake_storage