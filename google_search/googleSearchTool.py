from fastapi import FastAPI, Query, Security, HTTPException
from typing import Optional, Union
from fastapi.security import APIKeyHeader
from llama_hub.tools.google_search import GoogleSearchToolSpec

app = FastAPI(
    title="Google Search API",
    description="This API allows users to perform Google searches and retrieve results directly through the Google Custom Search JSON API."
)

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


@app.get('/google_search', summary='Perform a Google search with the provided query',
         response_description='The search results')
async def google_search(
        query: str = Query(..., description='The query string to search for'),
        engine_id: str = Query(..., description='Search engine ID for Google Custom Search'),
        num: Optional[int] = Query(10, description='Number of search results to return', ge=1, le=10),
        api_key: str = Security(get_api_key),
) -> Union[str, dict]:
    tool_spec = GoogleSearchToolSpec(api_key, engine_id, num)

    try:
        search_results = tool_spec.google_search(query)
        results = [result.get_content() for result in search_results]
        return {"results": results}
    except ValueError as e:
        return {"error": "ValueError", "message": str(e)}
    except Exception as e:
        return {"error": "ServerError", "message": "An error occurred while processing the request."}
