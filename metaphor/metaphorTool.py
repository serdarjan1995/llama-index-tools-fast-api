from fastapi import FastAPI, Query, HTTPException, Security
from typing import List, Optional

from fastapi.security import APIKeyHeader
from llama_hub.tools.metaphor import MetaphorToolSpec

app = FastAPI(
    title="Metaphor Search API",
    description="This API provides a set of endpoints to interact with the Metaphor search system, allowing users to perform various types of internet searches.",
)

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


@app.get('/search', summary='Search the Internet with a natural language query', tags=['Search'])
async def search(
        api_key: str = Security(get_api_key),
        query: str = Query(..., description='Natural language query string.'),
        num_results: Optional[int] = Query(10, description='Number of results to return.'),
        include_domains: Optional[List[str]] = Query(None,
                                                     description='List of top level domains to include in search.'),
        exclude_domains: Optional[List[str]] = Query(None,
                                                     description='List of top level domains to exclude from search.'),
        start_published_date: Optional[str] = Query(None, description='Start date to filter results (YYYY-MM-DD).'),
        end_published_date: Optional[str] = Query(None, description='End date to filter results (YYYY-MM-DD).')
) -> str:
    metaphor_tool = MetaphorToolSpec(api_key=api_key)
    return metaphor_tool.search(query, num_results, include_domains, exclude_domains, start_published_date,
                                end_published_date)


@app.get('/find-similar', summary='Find similar documents to a given URL', tags=['Search'])
async def find_similar(
        api_key: str = Security(get_api_key),
        url: str = Query(..., description='The web page URL to find similar results for.'),
        num_results: Optional[int] = Query(3, description='Number of results to return.'),
        start_published_date: Optional[str] = Query(None, description='Start date to filter results (YYYY-MM-DD).'),
        end_published_date: Optional[str] = Query(None, description='End date to filter results (YYYY-MM-DD).')
) -> str:
    metaphor_tool = MetaphorToolSpec(api_key=api_key)
    return metaphor_tool.find_similar(url, num_results, start_published_date, end_published_date)


@app.get('/retrieve_documents', summary='Retrieve documents by ids', tags=['Retrieve'])
async def current_date(api_key: str = Security(get_api_key), query: List[str] = Query(..., description='List of ids'),):
    metaphor_tool = MetaphorToolSpec(api_key=api_key)
    return metaphor_tool.retrieve_documents(ids=query)


@app.get('/search_and_retrieve', summary='Search and retrieve documents with a natural language query',
         tags=['Search', 'Retrieve'])
async def search_and_retrieve_documents(
        api_key: str = Security(get_api_key),
        query: str = Query(..., description='Natural language query string.'),
        num_results: Optional[int] = Query(10, description='Number of results to return.'),
        include_domains: Optional[List[str]] = Query(None,
                                                     description='List of top level domains to include in search.'),
        exclude_domains: Optional[List[str]] = Query(None,
                                                     description='List of top level domains to exclude from search.'),
        start_published_date: Optional[str] = Query(None, description='Start date to filter results (YYYY-MM-DD).'),
        end_published_date: Optional[str] = Query(None, description='End date to filter results (YYYY-MM-DD).')
) -> str:
    metaphor_tool = MetaphorToolSpec(api_key=api_key)
    return metaphor_tool.search_and_retrieve_documents(query, num_results, include_domains, exclude_domains,
                                                       start_published_date, end_published_date)
