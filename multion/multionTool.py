from fastapi import FastAPI, Query, HTTPException, Security, Depends
from typing import Optional
from pydantic import BaseModel
from llama_hub.tools.multion import MultionToolSpec

app = FastAPI()


class BrowseResponse(BaseModel):
    url: str
    status: str
    action_completed: str
    content: str


def get_token(header_token: Optional[str] = Security(...)):
    if header_token is None:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return header_token


@app.post('/browse', response_model=BrowseResponse, summary='Browse the web using Multion',
          description='Control web browsers using natural language with Multion',
          responses={200: {'description': 'The result of the browsing action'}})
async def browse(instruction: str = Query(..., description='Natural language instruction for web browsing'),
                 token: str = Depends(get_token)):
    tool = MultionToolSpec(token_file=None)
    result = tool.browse(instruction=instruction)
    return result
