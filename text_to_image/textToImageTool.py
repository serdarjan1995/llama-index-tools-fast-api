from fastapi import FastAPI, HTTPException, Security
from typing import Optional
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from llama_hub.tools.text_to_image import TextToImageToolSpec

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class GenerateImagesInput(BaseModel):
    prompt: str = Field(..., description='The prompt to generate an image(s) based on')
    n: Optional[int] = Field(1, description='The number of images to generate. Defaults to 1.')
    size: Optional[str] = Field('256x256',
                                description='The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512')


class GenerateImageVariationInput(BaseModel):
    url: str = Field(..., description='The url of the image to create a variation of')
    n: Optional[int] = Field(1, description='The number of images to generate. Defaults to 1.')
    size: Optional[str] = Field('256x256',
                                description='The size of the image(s) to generate. Defaults to 256x256. Other accepted values are 1024x1024 and 512x512')


@app.post('/generate_images/', summary='Generate image(s) based on text prompt')
def generate_images(generate_image_request: GenerateImagesInput, api_key: str = Security(get_api_key), ):
    try:
        tool_spec = TextToImageToolSpec(api_key=api_key)
        return tool_spec.generate_images(prompt=generate_image_request.prompt, n=generate_image_request.n,
                                         size=generate_image_request.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/generate_image_variation/', summary='Generate variations of an image')
def generate_image_variation(generate_image_variation_request: GenerateImageVariationInput,
                             api_key: str = Security(get_api_key), ):
    try:
        tool_spec = TextToImageToolSpec(api_key=api_key)
        return tool_spec.generate_image_variation(url=generate_image_variation_request.url,
                                                  n=generate_image_variation_request.n,
                                                  size=generate_image_variation_request.size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
