# BigDataIAAssignment2

Project Overview
Findata Inc. is building a master financial statement database to support analysts in conducting fundamental analysis of US public companies. This project involves scraping SEC financial data, designing Snowflake storage solutions, transforming data using DBT, automating pipelines with Airflow, and developing a Streamlit app with a FastAPI backend.

Folders 

Frontend - Contains all the Frontend Streamlit Files.

Dags - Contains all the Pipelines.

Backend - containst the fastapi code and dockerfile for deployment.

Zip to Json - Contains Code to convert data to json format.

DataScraping - Contains the code for Datascraping from sec website. This was a POC to check if all the files are downloading.

finddata_dbt - Contains the DBT file.

scripts - Contains the script to download the sec_data.py


Codelabs Preview -  https://codelabs-preview.appspot.com/?file_id=1sx8sjw3jT-GHpvyWU8EhqmGskVg990px71K6oIC8Jbw

https://docs.google.com/document/d/1sx8sjw3jT-GHpvyWU8EhqmGskVg990px71K6oIC8Jbw/edit?tab=t.0#heading=h.ujsqlibfh6ty

Technology Stack
Database: Snowflake
ETL & Pipelines: DBT, Apache Airflow, S3
Backend: FastAPI
Frontend: Streamlit
Infrastructure: Docker, SQLAlchemy

Step-by-Step Guide
1.Clone Repository & Install Dependencies
2.Data Ingestion & Processing
3.Scrape SEC Data & Download Datasets
4.Deploy & Run Airflow Pipelines
5.Run the Backend API
6.Run the Streamlit Frontend
7.Accessing Deployed Applications

Backend url:https://fastapi-snowflake-343736309329.us-central1.run.app
Frontend url:https://singhriya23-bigdataiaassignmen-frontendsnowflake-getdata-oefn0f.streamlit.app/


![sec_data_processing_pipelines](https://github.com/user-attachments/assets/adb572b8-2bd2-401c-af92-69199de77e64)





For Raw Staging,  we have developed a script to extract the files from the website, stage it to s3 and load data from s3 to snowflake.



For Json Staging,the scraped files are converted into json using scripts, then staged to s3, then uploaded to snowflake. However, the script puts the data into tsv rather than json format, so some transformations are done so that json is flattened.



For Dbt, we run the dbt to create denormalized tables in Snowflake.


Finally, FastAPI is used to connect to the snowflake to retrieve data and a client facing application using streamlit is done to view the data.









