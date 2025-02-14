import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# FastAPI backend URL
FASTAPI_URL = "https://fastapi-snowflake-343736309329.us-central1.run.app/execute_query/"

st.title("SQL Query Executor and Visualizer")

# Function to fetch and process query results
def fetch_query_results(query):
    response = requests.get(FASTAPI_URL, params={"sql_query": query})
    
    if response.status_code == 200:
        data = response.json().get("data", [])
        if not data:
            st.warning("No data returned for the query.")
            return None
        df = pd.DataFrame(data)
        df.columns = df.columns.str.upper()  
        return df
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        return None

#Query 1
fixed_query = """
SELECT TOP 10 name, revenue
FROM (
    SELECT s.name, n.value AS revenue
    FROM FIN_DATA.DEV.RAW_NUM n
    JOIN FIN_DATA.DEV.RAW_SUB s ON n.adsh = s.adsh
    WHERE n.tag = 'Revenues' 
      AND n.value IS NOT NULL
    ORDER BY n.value DESC
    LIMIT 100  
) AS top_100
ORDER BY revenue DESC; 
"""

if st.button("Run Top 10 Revenue Query"):
    df = fetch_query_results(fixed_query)
    if df is not None:
        df["REVENUE"] = pd.to_numeric(df["REVENUE"], errors="coerce")

        st.write("### Top 10 Companies by Revenue")
        st.dataframe(df)

        fig = px.bar(
            df, x="NAME", y="REVENUE",
            title="Top 10 Companies by Revenue",
            labels={"NAME": "Company", "REVENUE": "Revenue ($)"},
            text_auto=True
        )
        st.plotly_chart(fig)

st.write("---")  

#Query 2
financial_query = """
SELECT CIK, TOTAL_ASSETS, TOTAL_LIABILITIES 
FROM FIN_DATA.DENORMALIZED_TABLES.BALANCE_SHEET
ORDER BY TOTAL_ASSETS DESC
LIMIT 10;
"""

if st.button("Run Financial Position Query"):
    df = fetch_query_results(financial_query)
    if df is not None:
        df["TOTAL_ASSETS"] = pd.to_numeric(df["TOTAL_ASSETS"], errors="coerce")
        df["TOTAL_LIABILITIES"] = pd.to_numeric(df["TOTAL_LIABILITIES"], errors="coerce")

        st.write("### Top 10 Companies: Assets vs. Liabilities")
        st.dataframe(df)

        fig = px.bar(
            df, x="CIK", y=["TOTAL_ASSETS", "TOTAL_LIABILITIES"],
            title="Total Assets vs. Total Liabilities",
            labels={"value": "Amount ($)", "CIK": "Company CIK"},
            barmode="group",
            text_auto=True
        )
        st.plotly_chart(fig)

st.write("---")  # Separator

# --- Custom Query Input ---
user_query = st.text_area("Enter your SQL Query:")

if st.button("Run Custom Query"):
    if user_query.strip():
        df = fetch_query_results(user_query)
        if df is not None:
            st.write("### Query Results:")
            st.dataframe(df)
    else:
        st.warning("Please enter a valid SQL query.")
