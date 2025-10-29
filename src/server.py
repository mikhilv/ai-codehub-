from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from .database import SnowflakeDB
from .nl_to_sql import NLtoSQL

app = FastAPI(title="MCP Server for Natural Language SQL Queries")

# Initialize components
nl_to_sql = NLtoSQL()
db = SnowflakeDB()

class Query(BaseModel):
    query: str

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]

@app.post("/query", response_model=QueryResponse)
async def process_query(query: Query):
    try:
        # Convert natural language to SQL
        sql_query = nl_to_sql.generate_sql(query.query)
        
        # Execute SQL query
        results = db.execute_query(sql_query)
        
        return QueryResponse(
            sql_query=sql_query,
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    db.close()