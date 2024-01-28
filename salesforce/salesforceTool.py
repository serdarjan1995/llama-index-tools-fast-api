from enum import Enum
from fastapi import FastAPI
from llama_hub.tools.salesforce import SalesforceToolSpec
from pydantic import BaseModel, Field

app = FastAPI(title="Salesforce API", description="API for executing SOSL and SOQL queries in Salesforce.",
              version="1.0.0")


class QueryTypeEnum(Enum):
    sosl = 'sosl'
    soql = 'soql'


class RequestData(BaseModel):
    query: str = Field(..., description='SOSL query string.')
    query_type: QueryTypeEnum = Field(QueryTypeEnum.sosl, description='Query Type')
    username: str = Field(..., description='Salesforce username.')
    password: str = Field(..., description='Salesforce password.')
    consumer_key: str = Field(..., description='Salesforce consumer key.')
    consumer_secret: str = Field(..., description='Salesforce consumer secret.')
    domain: str = Field(..., description='Salesforce domain')


def get_salesforce_connection(username: str, password: str, consumer_key: str, consumer_secret: str, domain: str):
    return SalesforceToolSpec(
        username=username,
        password=password,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        domain=domain
    )


@app.post('/execute/', summary='Execute a query in Salesforce', tags=['Salesforce'])
def execute(request_data: RequestData):
    sf = get_salesforce_connection(request_data.username, request_data.password, request_data.consumer_key,
                                   request_data.consumer_secret, request_data.domain)
    try:
        if request_data.query_type == QueryTypeEnum.sosl:
            return sf.execute_sosl(request_data.query)
        elif request_data.query_type == QueryTypeEnum.soql:
            return sf.execute_soql(request_data.query)
        return {}
    except Exception as e:
        return {"error": "Query execution failed", "message": str(e)}
