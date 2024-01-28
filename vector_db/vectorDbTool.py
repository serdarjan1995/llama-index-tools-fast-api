from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from llama_hub.tools.vector_db import VectorDBToolSpec

app = FastAPI()


class AutoRetrieveRequest(BaseModel):
    index: str
    query: str
    top_k: int
    filter_key_list: List[str]
    filter_value_list: List[str]


@app.post('/auto_retrieve', response_model=str, summary='Auto-retrieve from a vector database')
def auto_retrieve(request: AutoRetrieveRequest):
    tool_spec = VectorDBToolSpec(index=request.index)
    return tool_spec.auto_retrieve_fn(
        query=request.query,
        top_k=request.top_k,
        filter_key_list=request.filter_key_list,
        filter_value_list=request.filter_value_list
    )
