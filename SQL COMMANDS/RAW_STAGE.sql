FIN_DATA.DEVcreate database fin_data;
create schema fin_data.dev;

CREATE OR REPLACE STORAGE INTEGRATION Snowflake_role
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'S3'
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::676206927597:role/Snowflake-role'
ENABLED = TRUE
STORAGE_ALLOWED_LOCATIONS = ('s3://s3-airflow-bucket-1/');

desc integration Snowflake_role;

CREATE OR REPLACE STAGE my_s3_stage
URL = 's3://s3-airflow-bucket-1/ceac_financial_statements'
STORAGE_INTEGRATION = Snowflake_role;

SHOW STAGES;

LIST @my_s3_stage;
LIST @my_s3_stage/2024q1/;
LIST @my_s3_stage/ceac_financial_statements/2024q1;


DESCRIBE STAGE my_s3_stage;
LIST @my_s3_stage/2024q1; -- Check if file exists
------------------------------------------------------------------------------------
SELECT * FROM @my_s3_stage/2024q1/sub.txt (FILE_FORMAT => my_csv_format) LIMIT 5; -- Preview file

SELECT * FROM RAW_pre where quarter="2024/Q2"; 

select * from raw_tag limit 5;
FIN_DATA.DEV.RAW_SUB

select * from raw_num

SELECT $1, $2, $3 FROM @my_s3_stage/2024q1/num.txt 
(FILE_FORMAT => (TYPE=CSV, FIELD_DELIMITER='\t', SKIP_HEADER=1)) LIMIT 5;

SELECT 
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, 
    $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, 
    $31, $32, $33, $34, $35, $36
FROM @my_s3_stage/2024q1/sub.txt 
(FILE_FORMAT => my_csv_format)
LIMIT 5;

DESC TABLE RAW_PRE;
DELETE FROM RAW_SUB;
DELETE FROM RAW_PRE;
DELETE FROM RAW_NUM;

ALTER TABLE FIN_DATA.DEV.RAW_tag
ADD COLUMN QUARTER VARCHAR(10);

UPDATE FIN_DATA.DEV.RAW_tag
SET QUARTER = '2024/Q1';


-----------------------------------------------------------------
CREATE OR REPLACE FILE FORMAT my_csv_format
TYPE = CSV
FIELD_DELIMITER = '\t'
SKIP_HEADER = 1;

COPY INTO RAW_SUB
FROM @my_s3_stage/2024q1/sub.txt
FILE_FORMAT = my_csv_format
FORCE = TRUE;

COPY INTO RAW_PRE
FROM @my_s3_stage/2024q1/pre.txt
FILE_FORMAT = my_csv_format
FORCE = TRUE;

COPY INTO RAW_TAG
FROM @my_s3_stage/2024q1/tag.txt
FILE_FORMAT = my_csv_format
FORCE = TRUE;

CREATE OR REPLACE FILE FORMAT my_csv_format_num
TYPE = CSV
FIELD_DELIMITER = '\t'
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ESCAPE = '\\'
TRIM_SPACE = TRUE
EMPTY_FIELD_AS_NULL = TRUE;


COPY INTO RAW_NUM
FROM @my_s3_stage/2024q1/num.txt
FILE_FORMAT = my_csv_format_num
FORCE = TRUE;

SELECT * FROM FIN_DATA.JSON_TABLES.Q1_OUTPUT LIMIT 5;


SELECT 
    json_data:adsh::STRING AS adsh,
    json_data:cik::STRING AS cik,
    json_data:name::STRING AS company_name
FROM FIN_DATA.JSON_TABLES.Q1_OUTPUT;


SELECT s.name, n.value AS revenue
FROM FIN_DATA.DEV.RAW_NUM n
JOIN FIN_DATA.DEV.RAW_SUB s ON n.adsh = s.adsh
WHERE n.tag = 'Revenues'
ORDER BY n.value DESC
LIMIT 10;

SELECT TOP 10 name, revenue
FROM (
    SELECT s.name, n.value AS revenue
    FROM FIN_DATA.DEV.RAW_NUM n
    JOIN FIN_DATA.DEV.RAW_SUB s ON n.adsh = s.adsh
    WHERE n.tag = 'Revenues' 
      AND n.value IS NOT NULL
    ORDER BY n.value DESC
    LIMIT 100  -- Get first 100 records
) AS top_100
ORDER BY revenue DESC;  -- Now get the top 10 from those 100


SELECT  s.name, n.value AS net_income
FROM FIN_DATA.DEV.RAW_NUM n
JOIN FIN_DATA.DEV.RAW_SUB s ON n.adsh = s.adsh
WHERE n.tag = 'NetIncomeLoss'
AND n.value IS NOT NULL
ORDER BY n.ddate LIMIT 20;




