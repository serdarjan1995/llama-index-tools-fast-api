from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from llama_hub.tools.neo4j_db import Neo4jQueryToolSpec
from llama_index.llms import OpenAI

app = FastAPI()


class Question(BaseModel):
    open_ai_key: str = Field('XXXX-XXXX', description='OpenAI api key')
    open_ai_model: str = Field('gpt-4', description='OpenAI model name')
    open_ai_temperature: int = Field(0, description='OpenAI temperature')
    neo4j_url: str = Field('', description='The connection string for the Neo4j database.')
    neo4j_user: str = Field('', description='Username for the Neo4j database.')
    neo4j_password: str = Field('', description='Password for the Neo4j database.')
    neo4j_database: str = Field('', description='Neo4j database.')
    validate_cypher: bool = Field(False, description='Validate relationship directions in the generated Cypher statement. Default: False')
    question: str = Field(..., description='The question to execute the Cypher query for.')
    history: Optional[List] = Field(None, description='A list of previous interactions for context. Defaults to None.')


@app.post('/query', response_model=List, name='Run Cypher Query',
          summary='Executes a Neo4j Cypher query based on user input')
def run_request(query: Question):
    try:
        llm_model = OpenAI(model=query.open_ai_model, openai_api_key=query.open_ai_key,
                           temperature=query.open_ai_temperature)

        neo4j_query_tool = Neo4jQueryToolSpec(
            url=query.neo4j_url,
            user=query.neo4j_user,
            password=query.neo4j_password,
            database=query.neo4j_database,
            llm=llm_model,
            validate_cypher=query.validate_cypher
        )

        response = neo4j_query_tool.run_request(query.question, query.history)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
