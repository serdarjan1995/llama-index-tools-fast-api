from fastapi import FastAPI, Query, HTTPException
from llama_hub.tools.chatgpt_plugin import ChatGPTPluginToolSpec
from pydantic import BaseModel


class Document(BaseModel):
    title: str
    content: str


app = FastAPI(title="ChatGPT Plugin API",
              description="This API provides endpoints for interacting with ChatGPT plugins, allowing users to load OpenAPI specifications of plugins and get descriptions of these plugins.")


@app.get('/load_openapi_spec', summary='Load OpenAPI Spec of the Plugin', tags=['Plugin'])
async def load_openapi_spec(
        manifest_url: str = Query(..., title='Manifest URL',
                                  description='URL of the plugin manifest to load the OpenAPI specification from.')
):
    plugin_spec = ChatGPTPluginToolSpec(manifest_url=manifest_url)

    try:
        openapi_spec_docs = plugin_spec.load_openapi_spec()
        return [doc.get_content() for doc in openapi_spec_docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/describe_plugin', summary='Describe the ChatGPT Plugin', tags=['Plugin'])
async def describe_plugin(
        manifest_url: str = Query(..., title='Manifest URL',
                                  description='URL of the plugin manifest to get the plugin description.')
):
    plugin_spec = ChatGPTPluginToolSpec(manifest_url=manifest_url)

    try:
        plugin_description = plugin_spec.describe_plugin()
        return plugin_description
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
