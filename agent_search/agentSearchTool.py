from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from agent_search_toolspec import AgentSearchToolSpec

app = FastAPI(title="Agent Search Tool")


class Document(BaseModel):
    text: str


class AgentSearchQueryResponse(BaseModel):
    results: list[Document]


api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_search_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class AgentSearchQuery(BaseModel):
    query: str = Field(..., description='Query to search')
    search_provider: Optional[str] = Field('bing', description='Query to search')
    llm_model: Optional[str] = Field('SciPhi/Sensei-7B-V1', description='Query to search')
    api_base: Optional[str] = Field('', description='Api base')


@app.post('/load_data/', summary='Search query', tags=['Query'])
async def load_data(request_data: AgentSearchQuery, api_key: str = Security(get_search_key)) -> list:
    try:
        tool_spec = AgentSearchToolSpec(api_base=request_data.api_base, api_key=api_key)

        search_results = tool_spec.load_data(query=request_data.query, search_provider=request_data.search_provider,
                                             llm_model=request_data.llm_model)

        return [doc.get_content() for doc in search_results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
