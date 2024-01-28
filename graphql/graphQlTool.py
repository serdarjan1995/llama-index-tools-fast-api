from fastapi import FastAPI
from pydantic import BaseModel
from llama_hub.tools.graphql import GraphQLToolSpec

app = FastAPI()


class GraphQLQuery(BaseModel):
    query: str
    variables: str
    operation_name: str
    headers: dict
    url: str


@app.post("/graphql_request", summary="Make a GraphQL query")
def graphql_request_endpoint(query_data: GraphQLQuery):
    """Make a GraphQL query against a server with the provided query, variables, and operation name.

    - **query**: The GraphQL query to execute
    - **variables**: The variable values for the query
    - **operation_name**: The name for the operation
    - **token**: The authorization token (if required for the endpoint)
    """
    tool = GraphQLToolSpec(url=query_data.url, headers=query_data.headers)
    response = tool.graphql_request(query_data.query, query_data.variables, query_data.operation_name)
    return response
