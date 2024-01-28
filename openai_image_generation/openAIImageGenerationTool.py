from fastapi import FastAPI, Header, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from llama_hub.tools.openai_image_generation import OpenAIImageGenerationToolSpec
from pydantic import BaseModel, Field

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class ImageGenerateRequest(BaseModel):
    text: str = Field(..., description='The text to generate an image from', max_length=100),
    model: str = Field('dall-e-3', description='The model to use to generate the image', max_length=10),
    quality: str = Field('standard', description='The quality of the image to generate', max_length=10),
    num_images: int = Field(1, description='The number of images to generate', ge=1, le=10),


@app.post('/image_generation/', summary='Generate an image from text using OpenAI DALL-E model')
def image_generation(
        request_data: ImageGenerateRequest,
        api_key: str = Security(get_api_key),
):
    try:
        tool_spec = OpenAIImageGenerationToolSpec(api_key=api_key)
        return tool_spec.image_generation(request_data.text, request_data.model, request_data.quality,
                                          request_data.num_images)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
