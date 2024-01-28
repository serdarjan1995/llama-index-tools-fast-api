from fastapi import FastAPI, HTTPException, Depends, Security, Form, UploadFile, File
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import uvicorn
from llama_hub.tools.cogniswitch import CogniswitchToolSpec
from pydantic import BaseModel

app = FastAPI()

cs_platform_token_header_auth = APIKeyHeader(name='cs-platform-token', auto_error=True, scheme_name='cs-platform-token')
cs_api_key_header_auth = APIKeyHeader(name='cs-api-key', auto_error=True, scheme_name='cs-api-key')
open_ai_api_key_header_auth = APIKeyHeader(name='openai-api-key', auto_error=True, scheme_name='openai-api-key')


class AccessKeys(BaseModel):
    cs_platform_token: str
    cs_api_key: str
    open_ai_api_key: str


async def get_api_key(cs_platform_token: str = Depends(cs_platform_token_header_auth),
                      cs_api_key: str = Depends(cs_api_key_header_auth),
                      open_ai_api_key: str = Depends(open_ai_api_key_header_auth)):
    if not cs_platform_token or not cs_api_key or not open_ai_api_key_header_auth:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return AccessKeys(cs_platform_token=cs_platform_token, cs_api_key=cs_api_key, open_ai_api_key=open_ai_api_key)


@app.post('/store_data', summary='Store data to the Cogniswitch service')
async def store_data(
        url: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        document_name: Optional[str] = Form(None),
        document_description: Optional[str] = Form(None),
        access_keys: AccessKeys = Depends(get_api_key)
):
    if not file and not url:
        raise HTTPException(status_code=400, detail='No input provided')
    elif file and url:
        raise HTTPException(status_code=400, detail='Too many inputs provided.')
    tool = CogniswitchToolSpec(cs_token=access_keys.cs_platform_token, apiKey=access_keys.cs_api_key,
                               OAI_token=access_keys.open_ai_api_key)
    result = tool.store_data(url=url, file=file.file if file else None, document_name=document_name,
                             document_description=document_description)
    return result


@app.post('/query_knowledge', summary='Query the Cogniswitch service for knowledge')
async def query_knowledge(
        query: str = Form(...),
        access_keys: AccessKeys = Depends(get_api_key)
):
    tool = CogniswitchToolSpec(cs_token=access_keys.cs_platform_token, apiKey=access_keys.cs_api_key,
                               OAI_token=access_keys.open_ai_api_key)
    result = tool.query_knowledge(query=query)
    return result


@app.get('/knowledge_status', summary='Check the status of stored knowledge')
async def knowledge_status(
        document_name: str,
        access_keys: AccessKeys = Depends(get_api_key)
):
    tool = CogniswitchToolSpec(cs_token=access_keys.cs_platform_token, apiKey=access_keys.cs_api_key,
                               OAI_token=access_keys.open_ai_api_key)
    result = tool.knowledge_status(document_name=document_name)
    return result


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
