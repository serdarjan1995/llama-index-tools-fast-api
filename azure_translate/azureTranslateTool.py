from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from llama_hub.tools.azure_translate import AzureTranslateToolSpec

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


class TranslateRequest(BaseModel):
    text: str = Field(..., description='Translate text to a target language')
    language: str = Field(..., description='Target Language')
    region: str = Field(..., description='Azure service region')


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


@app.post('/translate', summary='Translate text to a specified language')
def translate_text(translate_request: TranslateRequest, api_key: str = Security(get_api_key)):
    azure_translate_tool = AzureTranslateToolSpec(api_key=api_key, region=translate_request.region)
    return azure_translate_tool.translate(text=translate_request.text, language=translate_request.language)
