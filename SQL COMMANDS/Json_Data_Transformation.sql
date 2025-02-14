WITH cleaned_data AS (
    SELECT 
        SPLIT_PART(TO_VARCHAR(JSON_CONTENT), '\n', 1) AS headers,  -- Extract column headers (first row)
        SPLIT(TO_VARCHAR(JSON_CONTENT), '\n') AS all_rows  -- Extract all data rows
    FROM Q1
),
data_rows AS (
    SELECT all_rows.value AS row_data
    FROM cleaned_data, LATERAL FLATTEN(input => all_rows) AS all_rows
    WHERE all_rows.index > 0  -- Skip the first row (headers)
)
SELECT 
    header_values.value AS column_name,  -- Extract column names from headers
    data_values.value AS column_value    -- Extract corresponding values from data rows
FROM cleaned_data, 
LATERAL FLATTEN(input => SPLIT(headers, '\t')) AS header_values,  -- Split headers into columns
data_rows,
LATERAL FLATTEN(input => SPLIT(data_rows.row_data, '\t')) AS data_values;  -- Split data into column values



CREATE OR REPLACE TABLE Q4_OUTPUT (
    json_data VARIANT  
);


INSERT INTO Q4_OUTPUT (json_data)
WITH cleaned_data AS (
    
    SELECT 
        SPLIT_PART(TO_VARCHAR(JSON_CONTENT), '\n', 1) AS headers,  
        SPLIT(TO_VARCHAR(JSON_CONTENT), '\n') AS all_rows  
    FROM Q4
),
data_rows AS (
    -- Extract data rows excluding the header row
    SELECT 
        all_rows.value AS row_data,
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS row_id  
    FROM cleaned_data
    CROSS JOIN TABLE(FLATTEN(input => all_rows)) AS all_rows
    WHERE all_rows.index > 0  
),
structured_data AS (
    
    SELECT 
        header_values.value AS column_name,  
        data_values.value AS column_value,
        data_rows.row_id  -- Unique row identifier
    FROM cleaned_data
    CROSS JOIN TABLE(FLATTEN(input => SPLIT(headers, '\t'))) AS header_values
    CROSS JOIN data_rows
    CROSS JOIN TABLE(FLATTEN(input => SPLIT(data_rows.row_data, '\t'))) AS data_values
    WHERE header_values.index = data_values.index  
),
json_output AS (
    
    SELECT 
        OBJECT_CONSTRUCT(
            'adsh', MAX(CASE WHEN column_name = 'adsh' THEN column_value END),
            'cik', MAX(CASE WHEN column_name = 'cik' THEN column_value END),
            'name', MAX(CASE WHEN column_name = 'name' THEN column_value END),
            'sic', MAX(CASE WHEN column_name = 'sic' THEN column_value END),
            'countryba', MAX(CASE WHEN column_name = 'countryba' THEN column_value END),
            'stprba', MAX(CASE WHEN column_name = 'stprba' THEN column_value END),
            'cityba', MAX(CASE WHEN column_name = 'cityba' THEN column_value END),
            'zipba', MAX(CASE WHEN column_name = 'zipba' THEN column_value END),
            'bas1', MAX(CASE WHEN column_name = 'bas1' THEN column_value END),
            'bas2', MAX(CASE WHEN column_name = 'bas2' THEN column_value END),
            'baph', MAX(CASE WHEN column_name = 'baph' THEN column_value END),
            'countryma', MAX(CASE WHEN column_name = 'countryma' THEN column_value END),
            'stprma', MAX(CASE WHEN column_name = 'stprma' THEN column_value END),
            'cityma', MAX(CASE WHEN column_name = 'cityma' THEN column_value END),
            'zipma', MAX(CASE WHEN column_name = 'zipma' THEN column_value END),
            'mas1', MAX(CASE WHEN column_name = 'mas1' THEN column_value END),
            'mas2', MAX(CASE WHEN column_name = 'mas2' THEN column_value END),
            'countryinc', MAX(CASE WHEN column_name = 'countryinc' THEN column_value END),
            'stprinc', MAX(CASE WHEN column_name = 'stprinc' THEN column_value END),
            'ein', MAX(CASE WHEN column_name = 'ein' THEN column_value END),
            'former', MAX(CASE WHEN column_name = 'former' THEN column_value END),
            'changed', MAX(CASE WHEN column_name = 'changed' THEN column_value END),
            'afs', MAX(CASE WHEN column_name = 'afs' THEN column_value END),
            'wksi', MAX(CASE WHEN column_name = 'wksi' THEN column_value END),
            'fye', MAX(CASE WHEN column_name = 'fye' THEN column_value END),
            'form', MAX(CASE WHEN column_name = 'form' THEN column_value END),
            'period', MAX(CASE WHEN column_name = 'period' THEN column_value END),
            'fy', MAX(CASE WHEN column_name = 'fy' THEN column_value END),
            'fp', MAX(CASE WHEN column_name = 'fp' THEN column_value END),
            'filed', MAX(CASE WHEN column_name = 'filed' THEN column_value END),
            'accepted', MAX(CASE WHEN column_name = 'accepted' THEN column_value END),
            'prevrpt', MAX(CASE WHEN column_name = 'prevrpt' THEN column_value END),
            'detail', MAX(CASE WHEN column_name = 'detail' THEN column_value END),
            'instance', MAX(CASE WHEN column_name = 'instance' THEN column_value END),
            'nciks', MAX(CASE WHEN column_name = 'nciks' THEN column_value END),
            'aciks', MAX(CASE WHEN column_name = 'aciks' THEN column_value END)
        ) AS json_data
    FROM structured_data
    GROUP BY row_id
)
SELECT json_data FROM json_output;


