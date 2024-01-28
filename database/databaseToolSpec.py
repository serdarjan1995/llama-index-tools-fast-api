from typing import List, Optional
from fastapi import FastAPI, HTTPException
from llama_hub.tools.database import DatabaseToolSpec
from pydantic import BaseModel, Field

app = FastAPI()


class DatabaseConfig(BaseModel):
    scheme: str = "postgres"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "FakeExamplePassword"
    dbname: str = "postgres"


class RequestBody(BaseModel):
    query: str = """SELECT CONCAT(name, ' is ', age, ' years old.') AS text FROM public.users WHERE age >= 18"""
    tables: Optional[List[str]] = Field(None, description="List of table names to describe"),
    connection_uri: Optional[str] = "{scheme}://{user}:{password}@{host}:{port}/{dbname}"
    db_config: Optional[DatabaseConfig] = None


@app.post("/load_data", summary="Load data from the database", )
async def read_load_data(request_body: RequestBody):
    try:
        if request_body.connection_uri:
            db_tool = DatabaseToolSpec(uri=request_body.connection_uri)
        else:
            db_tool = DatabaseToolSpec(**request_body.db_config.model_dump())
        documents = db_tool.load_data(request_body.query)
        return documents
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/list_tables", summary="List all tables in the database", )
async def read_list_tables(request_body: RequestBody):
    try:
        if request_body.connection_uri:
            db_tool = DatabaseToolSpec(uri=request_body.connection_uri)
        else:
            db_tool = DatabaseToolSpec(**request_body.db_config.model_dump())
        tables = db_tool.list_tables()
        return tables
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/describe_tables", summary="Describe tables in the database", )
async def read_describe_tables(request_body: RequestBody):
    try:
        if request_body.connection_uri:
            db_tool = DatabaseToolSpec(uri=request_body.connection_uri)
        else:
            db_tool = DatabaseToolSpec(**request_body.db_config.model_dump())
        description = db_tool.describe_tables(request_body.tables)
        return description
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
