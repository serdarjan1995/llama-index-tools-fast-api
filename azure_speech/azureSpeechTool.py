from typing import List
from fastapi import FastAPI, HTTPException, Security
from llama_hub.tools.azure_speech import AzureSpeechToolSpec
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class TextToSpeechRequest(BaseModel):
    text: str = Field(..., description='The text to convert to speech')
    region: str = Field(..., description='Azure service region')
    language: str = Field('en-US', description='Language for the speech')


class SpeachToTextRequest(BaseModel):
    filename: str = Field(..., description='The filename of the audio file to transcribe')
    region: str = Field(..., description='Azure service region')
    language: str = Field('en-US', description='Language for the speech')


@app.post('/text_to_speech', summary='Convert text to speech', response_model=str)
async def convert_text_to_speech(request: TextToSpeechRequest, api_key: str = Security(get_api_key)):
    speech_tool = AzureSpeechToolSpec(speech_key=api_key, region=request.region, language=request.language)
    return speech_tool.text_to_speech(request.text)


@app.post('/speech_to_text', summary='Convert speech to text', response_model=List[str])
async def convert_speech_to_text(request: SpeachToTextRequest, api_key: str = Security(get_api_key)):
    speech_tool = AzureSpeechToolSpec(speech_key=api_key, region=request.region, language=request.language)
    return speech_tool.speech_to_text(request.filename)
