from enum import Enum
from fastapi import FastAPI, HTTPException, Security
from llama_hub.tools.bing_search import BingSearchToolSpec
from pydantic import BaseModel, Field
from typing import List
from fastapi.security.api_key import APIKeyHeader

app = FastAPI(title='Bing Search Tool')

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class SearchTypeEnum(Enum):
    news = 'news'
    image = 'image'
    video = 'video'


class QueryRequest(BaseModel):
    query: str = Field(..., description='Query to search')
    search_type: SearchTypeEnum = Field(SearchTypeEnum.news, description='Search type')


@app.post('/search', response_model=List, summary='Search using Bing',
          description='Returns a list of search results for a given query.')
def bing_news_search(query: QueryRequest, api_key: str = Security(get_api_key)):
    tool = BingSearchToolSpec(api_key=api_key)
    if query.search_type == SearchTypeEnum.news:
        return tool.bing_news_search(query.query)
    elif query.search_type == SearchTypeEnum.video:
        return tool.bing_video_search(query.query)
    elif query.search_type == SearchTypeEnum.image:
        return tool.bing_image_search(query.query)
    else:
        raise NotImplementedError()
