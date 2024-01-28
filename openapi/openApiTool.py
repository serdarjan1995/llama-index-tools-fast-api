from fastapi import FastAPI, Query
from typing import Union
from llama_hub.tools.openapi import OpenAPIToolSpec

app = FastAPI(
    title="OpenAPI Tool",
    description="API for loading and interacting with OpenAPI specifications.",
)


@app.get('/load-openapi-spec', response_model=dict, summary='Load OpenAPI Specification', tags=['OpenAPI Tool'])
async def load_openapi_spec(
        url: str = Query(None, description='The OpenAPI specification URL.')
) -> Union[str, dict]:
    try:
        tool_spec = OpenAPIToolSpec(url=url)
        return tool_spec.load_openapi_spec()[0].get_content()
    except Exception as e:
        return {"error": "An error occurred", "message": str(e)}
