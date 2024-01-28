from fastapi import FastAPI, Query, Depends, HTTPException
from typing import Optional

from fastapi.security import APIKeyHeader
from llama_hub.tools.yelp import YelpToolSpec
from pydantic import BaseModel, Field

app = FastAPI(
    title="Yelp Business API",
    description="API for searching businesses and fetching reviews using Yelp.",
)

api_key_header = APIKeyHeader(name='Api-key', auto_error=True, scheme_name='api-key')
client_id_header = APIKeyHeader(name='Client-Id', auto_error=True, scheme_name='client-id')


class ApiKeys(BaseModel):
    api_key: str
    client_id: str


async def get_api_key(api_key: str = Depends(api_key_header),
                      client_id: str = Depends(client_id_header)):
    if not api_key or not client_id:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return ApiKeys(api_key=api_key, client_id=client_id)


class SearchRequest(BaseModel):
    query: str = Field(..., description='Search term or business name')
    location: str = Field(..., description='Location to search within')
    radius: Optional[int] = Field(None, description='Search radius in meters')


class ReviewRequest(BaseModel):
    business_id: str = Field(..., description='The business ID obtained from search')


@app.post('/business/search', summary='Search for businesses based on a query', tags=['Business Search'])
async def business_search(search_reqeust: SearchRequest, api_keys: ApiKeys = Depends(get_api_key)):
    tool_spec = YelpToolSpec(api_key=api_keys.api_key, client_id=api_keys.client_id)
    try:
        results = tool_spec.business_search(location=search_reqeust.location, term=search_reqeust.query,
                                            radius=search_reqeust.radius)
        return {"results": [result.get_content() for result in results]}
    except Exception as e:
        return {"error": str(e)}


@app.post('/business/reviews', summary='Fetch reviews for a specific business by ID', tags=['Business Reviews'])
async def business_reviews(review_request: ReviewRequest, api_keys: ApiKeys = Depends(get_api_key)):
    tool_spec = YelpToolSpec(api_key=api_keys.api_key, client_id=api_keys.client_id)
    try:
        reviews = tool_spec.business_reviews(id=review_request.business_id)
        return {"reviews": [review.get_content() for review in reviews]}
    except Exception as e:
        return {"error": str(e)}
