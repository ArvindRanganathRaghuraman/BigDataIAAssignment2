from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

app = FastAPI()

#snowflake credentials
SNOWFLAKE_USER = "ARVIND177"
SNOWFLAKE_PASSWORD = quote_plus("Arvind@177")  # Encodes special characters
SNOWFLAKE_ACCOUNT = "duvvjid-bvb83781"
SNOWFLAKE_DATABASE = "FIN_DATA"
SNOWFLAKE_SCHEMA = "DEV"
SNOWFLAKE_WAREHOUSE = "WAREHOUSE_STORE"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"

SNOWFLAKE_URL = (
    f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/"
    f"{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}&role={SNOWFLAKE_ROLE}"
)

# creating an engine for sql alchemy
engine = create_engine(SNOWFLAKE_URL)
SessionLocal = sessionmaker(bind=engine)

#getting a session from alchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#checking the sql connection
@app.get("/check_connection/")
def check_connection(db: SessionLocal = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Connected to Snowflake!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Snowflake connection failed: {str(e)}")

#query input for accessing data from snowflake
@app.get("/execute_query/")
def execute_query(sql_query: str = Query(..., title="SQL Query"), db: SessionLocal = Depends(get_db)):
    """Allows users to enter a SQL query and execute it in Snowflake."""
    try:
        sql = text(sql_query)
        result = db.execute(sql)
        rows = result.fetchall()
        columns = result.keys()  
        
        # Format data as JSON
        data = [dict(zip(columns, row)) for row in rows]
        return {"status": "success", "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
