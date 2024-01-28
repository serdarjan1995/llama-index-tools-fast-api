from fastapi import FastAPI, Query, HTTPException, Security
from fastapi.security import APIKeyHeader
from llama_hub.tools.tavily_research import TavilyToolSpec
from typing import Optional

app = FastAPI(
    title="Tavily Research API",
    description="API for searching and retrieving information using the Tavily Research tool.",
)

api_key_header = APIKeyHeader(name='Api-key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


@app.get('/search', summary='Search for relevant information', tags=['Search'])
async def search(
        query: str = Query(..., description='The query to search for.'),
        max_results: Optional[int] = Query(6, description='The maximum number of results to return.'),
        api_key: str = Security(get_api_key),
) -> dict:
    try:
        tavily_tool = TavilyToolSpec(api_key=api_key)
        documents = tavily_tool.search(query, max_results)
        return {"results": [{"url": doc.get_metadata_str().lstrip('"url: '), "text": doc.get_content()} for doc in
                            documents]}
    except Exception as e:
        return {"error": str(e)}
