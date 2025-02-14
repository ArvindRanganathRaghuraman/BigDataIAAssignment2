# BigDataIAAssignment2

ATTESTATION 
 WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENT'S WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

CONTRIBUTION 
KAUSHIK - DBT, Denormalized Tables Storage,Astro Db  - 33% 
RIYA - Raw Storage, Backend -Fastapi, Frontend - Streamlit, Airflow Pipeline for Raw Storage,Documentation 33% 
ARVIND - Json Converter, Airflow Pipeline for Json, Deployment, Diagrams 33%

Folders 

Frontend - Contains all the Frontend Streamlit Files.

Dags - Contains all the Pipelines.

Backend - containst the fastapi code and dockerfile for deployment.

Zip to Json - Contains Code to convert data to json format.

DataScraping - Contains the code for Datascraping from sec website. This was a POC to check if all the files are downloading.

finddata_dbt - Contains the DBT file.

scripts - Contains the script to download the sec_data.py


Codelabs Preview -  https://docs.google.com/document/d/1sx8sjw3jT-GHpvyWU8EhqmGskVg990px71K6oIC8Jbw/edit?usp=sharing.



![data_pipeline](https://github.com/user-attachments/assets/619eeeb6-bf9e-4296-9c86-75d8070668a2)


For Raw Staging,  we have developed a script to extract the files from the website, stage it to s3 and load data from s3 to snowflake.


![json_pipeline](https://github.com/user-attachments/assets/9bfca83b-6073-48af-91fe-b9ac8c7ddf2a) 

For Json Staging,the scraped files are converted into json using scripts, then staged to s3, then uploaded to snowflake. However, the script puts the data into tsv rather than json format, so some transformations are done so that json is flattened.

![tables_pipeline](https://github.com/user-attachments/assets/c3ca277e-fd33-450c-91b3-4f2246878214)

For Dbt, we run the dbt to create denormalized tables in Snowflake.


Finally, FastAPI is used to connect to the snowflake to retrieve data and a client facing application using streamlit is done to view the data.







