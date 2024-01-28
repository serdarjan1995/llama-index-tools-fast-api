from fastapi import FastAPI, Query, Security, HTTPException
from fastapi.security import APIKeyHeader

from llama_hub.tools.wolfram_alpha import WolframAlphaToolSpec

app = FastAPI(
    title="Wolfram Alpha Query API",
    description="API for querying Wolfram Alpha to get answers to mathematical or scientific questions.",
    version="1.0.0"
)

api_key_header = APIKeyHeader(name='Api-key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


@app.get('/wolfram/query', summary='Get result of a Wolfram Alpha query', tags=['Wolfram Alpha Query'])
async def wolfram_alpha_query(
        query: str = Query(..., description='The mathematical or scientific question to query.'),
        api_key: str = Security(get_api_key)
) -> dict:
    wolfram_spec = WolframAlphaToolSpec(app_id=api_key)
    return wolfram_spec.wolfram_alpha_query(query=query)
