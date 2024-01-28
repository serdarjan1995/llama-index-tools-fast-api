from fastapi import FastAPI, HTTPException, Query, Security
from typing import List, Optional

from fastapi.security import APIKeyHeader
from llama_hub.tools.notion import NotionToolSpec
from pydantic import BaseModel, Field

app = FastAPI(
    title='Notion Tool API',
    description='This API provides endpoints for interacting with Notion, including loading pages or databases, searching for content, and appending data to pages or blocks.',
)

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class AppendDataRequest(BaseModel):
    block_id: str = Field(..., description='ID of the Notion block or page to append content to.'),
    content: str = Field(..., description='Text content to append.'),
    text_type: Optional[str] = Field('paragraph', description='Type of text content, e.g., paragraph.'),


@app.get('/read-page', summary='Read notion page',
         description='Read notion page with given page_id')
async def load_data(
        page_id: str = Query(None, description='The Notion page ID to read.'),
        api_key: str = Security(get_api_key),
):
    tool_spec = NotionToolSpec(integration_token=api_key)

    try:
        documents = tool_spec.read_page(page_id=page_id)
        return {'data': documents}
    except Exception as e:
        return {"error": str(e)}


@app.get('/query-database', summary='Query notion database',
         description='Queries a notion database with given database_id')
async def load_data(
        database_id: str = Query(None, description='The Notion database ID to load.'),
        api_key: str = Security(get_api_key),
):
    tool_spec = NotionToolSpec(integration_token=api_key)

    try:
        documents = tool_spec.query_database(database_id=database_id)
        return {'data': documents}
    except Exception as e:
        return {"error": str(e)}


@app.get('/load', summary='Load Notion pages or databases',
         description='Loads a list of pages or databases given their IDs or a single database ID.')
async def load_data(
        page_ids: Optional[List[str]] = Query([], description='List of Notion page IDs to load.'),
        database_id: Optional[str] = Query(None, description='The Notion database ID to load.'),
        api_key: str = Security(get_api_key),
):
    tool_spec = NotionToolSpec(integration_token=api_key)
    if not page_ids and not database_id:
        return {"error": "page_ids or database_id must be provided"}

    try:
        documents = tool_spec.load_data(page_ids=page_ids, database_id=database_id)
        return {'data': [doc.get_content() for doc in documents]}
    except Exception as e:
        return {"error": str(e)}


@app.get('/search', summary='Search for Notion pages or databases',
         description='Searches for matching pages or databases based on the query.')
async def search_data(
        query: str = Query(..., description='Query string for searching Notion pages or databases.'),
        api_key: str = Security(get_api_key),
):
    tool_spec = NotionToolSpec(integration_token=api_key)
    try:
        page_ids = tool_spec.search_data(query)
        return {'page_ids': page_ids}
    except Exception as e:
        return {"error": str(e)}


@app.post('/append', summary='Append content to a Notion page or database',
          description='Appends text content to the end of the specified Notion page or block.')
async def append_data(
        request_data: AppendDataRequest,
        api_key: str = Security(get_api_key),
):
    tool_spec = NotionToolSpec(integration_token=api_key)
    try:
        append_result = tool_spec.append_data(block_id=request_data.block_id, content=request_data.content,
                                              text_type=request_data.text_type)
        if append_result == 'success':
            return {'status': 'Content appended successfully'}
        else:
            return {'status': 'Failed to append content', 'note': append_result}
    except Exception as e:
        return {"error": str(e)}
