from diagrams import Diagram
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import S3
from diagrams.saas.analytics import Snowflake
from diagrams.onprem.analytics import Dbt
from diagrams.custom import Custom

with Diagram("Tables Pipeline",show=False):
    raw_storage = Custom("Raw Data","raw_data.jpg")
    dbt_tool = Dbt("DBT")
    

    snowflake_storage = Snowflake("Snowflake")

    raw_storage >> dbt_tool>> snowflake_storage