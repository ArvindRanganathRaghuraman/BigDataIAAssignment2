import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
FASTAPI_URL = "https://fastapi-snowflake-343736309329.us-central1.run.app/execute_query/"

st.title("SQL Query Executor")


sql_query = st.text_area("Enter your SQL Query:")


if st.button("Run Query"):
    if sql_query.strip():
       
        response = requests.get(FASTAPI_URL, params={"sql_query": sql_query})
        
        if response.status_code == 200:
            data = response.json()["data"]
            
        
            df = pd.DataFrame(data)

            if not df.empty:
                st.write("### Query Results:")
                st.dataframe(df)  
            else:
                st.warning("No data returned for the query.")
        else:
            st.error(f"Error: {response.json()['detail']}")
    else:
        st.warning("Please enter a valid SQL query.")
