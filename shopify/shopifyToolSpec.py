from fastapi import FastAPI
from pydantic import BaseModel, Field
from llama_hub.tools.shopify import ShopifyToolSpec

app = FastAPI()


class RequestData(BaseModel):
    shop_url: str = Field(..., description='Shopify shop url')
    api_version: str = Field(..., description='Shopify api version to use')
    admin_api_key: str = Field(..., description='Shopify admin api key')
    query: str = Field(..., description='GraphQL query to execute')


@app.post('/query', summary='Execute a GraphQL query on the Shopify Admin API')
def run_graphql_query(request_data: RequestData):
    """
    - **query**: The GraphQL query string to be executed.
    """
    tool_spec = ShopifyToolSpec(shop_url=request_data.shop_url, api_version=request_data.api_version,
                                admin_api_key=request_data.admin_api_key)

    return tool_spec.run_graphql_query(request_data.query)
