from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from llama_hub.tools.arxiv import ArxivToolSpec

app = FastAPI()


class Document(BaseModel):
    text: str


class ArxivQueryResponse(BaseModel):
    results: list[Document]


@app.get('/arxiv/search/', summary='Search arXiv for papers related to a query', tags=['Arxiv Search'])
async def arxiv_search(
        topic: str = Query(..., description='The search query for the ArXiv papers.'),
        sort_by: Optional[str] = Query('relevance', description='Sort the results by relevance or date submitted.'),
        max_results: Optional[int] = Query(3,
                                           description='Maximum number of results to return.')) -> list:
    try:
        tool_spec = ArxivToolSpec(max_results=max_results)

        search_results = tool_spec.arxiv_query(topic, sort_by)

        return [doc.get_content() for doc in search_results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
