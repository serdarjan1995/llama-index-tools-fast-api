from typing import Optional
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from llama_hub.tools.playgrounds_subgraph_inspector import PlaygroundsSubgraphInspectorToolSpec
from pydantic import BaseModel, Field

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-Key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class QueryRequest(BaseModel):
    identifier: str = Field(..., description='Subgraph identifier or Deployment ID.')
    use_deployment_id: bool = Field(False,
                                    description='Flag to indicate if the identifier is a deployment ID. Default is False.')
    query: str = Field(..., description='The GraphQL query string to execute.')
    variables: Optional[dict] = Field(dict, description='Variables for the GraphQL query. Default is None.')
    operation_name: Optional[str] = Field(None,
                                          description='Name of the operation, if multiple operations are present in the query. Default is None.')


@app.post("/introspect_and_summarize_subgraph")
async def introspect_and_summarize_subgraph(query_request: QueryRequest, api_key: str = Security(get_api_key)):
    """Introspect and summarize a subgraph schema from The Graph's decentralized network."""
    inspector = PlaygroundsSubgraphInspectorToolSpec(identifier=query_request.identifier, api_key=api_key,
                                                     use_deployment_id=query_request.use_deployment_id)
    summary = inspector.introspect_and_summarize_subgraph()
    if 'Error' in summary:
        raise HTTPException(status_code=400, detail=summary)
    return {"summary": summary}
