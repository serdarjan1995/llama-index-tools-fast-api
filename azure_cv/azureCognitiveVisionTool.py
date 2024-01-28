from fastapi import FastAPI, Depends, Security, HTTPException, status, Query
from typing import List

from fastapi.security import APIKeyHeader
from llama_hub.tools.azure_cv import AzureCVToolSpec
from pydantic import BaseModel, Field

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_search_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class ImageAnalysisRequest(BaseModel):
    url: str
    features: List[str]
    resource: str = Field(..., description='Resource name')


@app.post('/process-image/', summary='Process an image', response_model=dict)
def process_image(image_request: ImageAnalysisRequest, api_key: str = Security(get_search_key)):
    azure_cv_tool = AzureCVToolSpec(resource=image_request.resource, api_key=api_key)
    return azure_cv_tool.process_image(url=image_request.url, features=image_request.features)
