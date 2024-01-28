from typing import Optional, Dict
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from llama_hub.tools.requests import RequestsToolSpec

app = FastAPI(title="Requests API", description="API for performing various HTTP requests.")

domain_headers_sample = {
    'api.openai.com': {
        "Authorization": "Bearer sk-your-key",
        "Content-Type": "application/json",
    }
}


class RequestData(BaseModel):
    url: str = Field(..., description='The url to make the get request against')
    query_params: Optional[dict] = Field(..., description='the parameters to provide with the get request')
    data: Optional[dict] = Field(..., description='the key-value pairs to provide with the get request')
    domain_headers: Optional[dict] = Field(domain_headers_sample,
                                           description='the key-value pairs to provide with the get request')


@app.post('/request/get', summary='Perform a GET request', tags=['Requests'])
async def get_request(request_data: RequestData):
    tool_spec = RequestsToolSpec(domain_headers=request_data.domain_headers)

    try:
        response = tool_spec.get_request(url=request_data.url, params=request_data.query_params)
        return response if not isinstance(response, str) else {"error": response}
    except Exception as e:
        return {"error": "Server Error", "message": str(e)}


@app.post('/request/post', summary='Perform a POST request', tags=['Requests'])
async def post_request(request_data: RequestData):
    tool_spec = RequestsToolSpec(domain_headers=request_data.domain_headers)

    try:
        response = tool_spec.post_request(url=request_data.url, data=request_data.data)
        return response if not isinstance(response, str) else {"error": response}
    except Exception as e:
        return {"error": "Server Error", "message": str(e)}


@app.post('/request/patch', summary='Perform a PATCH request', tags=['Requests'])
async def patch_request(request_data: RequestData):
    tool_spec = RequestsToolSpec(domain_headers=request_data.domain_headers)

    try:
        response = tool_spec.patch_request(url=request_data.url, data=request_data.data)
        return response if not isinstance(response, str) else {"error": response}
    except Exception as e:
        return {"error": "Server Error", "message": str(e)}
