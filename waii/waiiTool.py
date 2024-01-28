from fastapi import FastAPI, Query, HTTPException, Security, Depends
from typing import Optional
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from llama_hub.tools.waii import WaiiToolSpec

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-key', auto_error=True, scheme_name='api-key')
database_key_header = APIKeyHeader(name='Database-key', auto_error=True, scheme_name='database-key')
waii_url_header = APIKeyHeader(name='Waii-Url', auto_error=True, scheme_name='waii-url')


class ApiKeys(BaseModel):
    api_key: str
    database_key: str
    waii_url: str


async def get_api_key(api_key: str = Depends(api_key_header),
                      database_key: str = Depends(database_key_header),
                      waii_url: str = Depends(waii_url_header)):
    if not api_key or not database_key or not waii_url:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return ApiKeys(api_key=api_key, database_key=database_key, waii_url=waii_url)


class AskRequest(BaseModel):
    ask: str = Field(..., description='A natural language question')


class DescribeQueryRequest(BaseModel):
    query: str = Field(..., description='A SQL query')
    question: str = Query(..., description='A natural language question which the people want to ask.')


class DiffQueryRequest(BaseModel):
    previous_query: str = Field(..., description='The previous SQL query')
    current_query: str = Field(..., description='The current SQL query')


class DescribeDatasetRequest(BaseModel):
    ask: str = Field(..., description='A natural language question on how to describe the dataset')
    schema_name: Optional[str] = Field(None,
                                       description='The schema name of the dataset to describe, excluding the database name')
    table_name: Optional[str] = Field(None,
                                      description='The table name of the dataset to describe, excluding the schema name')


class TranscodeRequest(BaseModel):
    instruction: Optional[str] = Field('', description='Instruction in natural language')
    source_dialect: Optional[str] = Field(None, description='Source dialect of the query')
    source_query: Optional[str] = Field(None, description='The SQL query to transcode')
    target_dialect: Optional[str] = Field(None, description='The target dialect for the query')


@app.post('/get_answer', summary='Get the answer to a natural language query',
          description='Generate a SQL query and run it against the database, returning the summarization of the answer.')
def get_answer(ask_request: AskRequest, api_keys: ApiKeys = Depends(get_api_key)):
    waii_tool = WaiiToolSpec(
        url=api_keys.waii_url,
        api_key=api_keys.api_key,
        database_key=api_keys.database_key
    )
    return waii_tool.get_answer(ask_request.ask)


@app.post('/describe_query', summary='Describe the provided SQL query',
          description='Describe a SQL query, returning the summarization of the answer.')
def describe_query(describe_request: DescribeQueryRequest, api_keys: ApiKeys = Depends(get_api_key)):
    waii_tool = WaiiToolSpec(
        url=api_keys.waii_url,
        api_key=api_keys.api_key,
        database_key=api_keys.database_key
    )
    return waii_tool.describe_query(describe_request.question, describe_request.query)


@app.post('/diff_query', summary='Diff two SQL queries',
          description='Diff two SQL queries, returning the summarization of the answer.')
def diff_query(diff_query_request: DiffQueryRequest, api_keys: ApiKeys = Depends(get_api_key)):
    waii_tool = WaiiToolSpec(
        url=api_keys.waii_url,
        api_key=api_keys.api_key,
        database_key=api_keys.database_key
    )
    return waii_tool.diff_query(diff_query_request.previous_query, diff_query_request.current_query)


@app.post('/describe_dataset', summary='Describe a dataset with a natural language query',
          description='Describe a dataset, potentially a table or schema, by answering a natural language question.')
def describe_dataset(describe_dataset_request: DescribeDatasetRequest, api_keys: ApiKeys = Depends(get_api_key)):
    waii_tool = WaiiToolSpec(
        url=api_keys.waii_url,
        api_key=api_keys.api_key,
        database_key=api_keys.database_key
    )
    return waii_tool.describe_dataset(describe_dataset_request.ask, describe_dataset_request.schema_name,
                                      describe_dataset_request.table_name)


@app.post('/transcode', summary='Transcode a SQL query from one dialect to another',
          description='Transcode a SQL query from one dialect to another, based on the given instructions and target dialect.')
def transcode(transcode_request: TranscodeRequest, api_keys: ApiKeys = Depends(get_api_key)):
    waii_tool = WaiiToolSpec(
        url=api_keys.waii_url,
        api_key=api_keys.api_key,
        database_key=api_keys.database_key
    )
    return waii_tool.transcode(transcode_request.instruction, transcode_request.source_dialect,
                               transcode_request.source_query, transcode_request.target_dialect)


@app.get('/get_semantic_contexts', summary='Get all pre-defined semantic contexts',
         description='Retrieve a list of all pre-defined semantic contexts.')
def get_semantic_contexts(api_keys: ApiKeys = Depends(get_api_key)):
    waii_tool = WaiiToolSpec(
        url=api_keys.waii_url,
        api_key=api_keys.api_key,
        database_key=api_keys.database_key
    )
    return waii_tool.get_semantic_contexts()
