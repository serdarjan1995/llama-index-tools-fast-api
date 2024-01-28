from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
from typing import Optional
from llama_hub.tools.playgrounds_subgraph_connector import PlaygroundsSubgraphConnectorToolSpec

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


@app.post('/graphql_request/')
def graphql_request(
        query_request: QueryRequest,
        api_key: str = Security(get_api_key),
):
    """Make a GraphQL query."""
    try:
        tool_spec = PlaygroundsSubgraphConnectorToolSpec(identifier=query_request.identifier, api_key=api_key,
                                                         use_deployment_id=query_request.use_deployment_id)

        return tool_spec.graphql_request(query=query_request.query, variables=query_request.variables,
                                         operation_name=query_request.operation_name)
    except ValueError as e:
        return {'error': f'Error decoding JSON: {e}'}
