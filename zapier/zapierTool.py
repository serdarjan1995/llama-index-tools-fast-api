from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.security import APIKeyHeader
from llama_hub.tools.zapier import ZapierToolSpec
from typing import Optional

from pydantic import BaseModel, Field

app = FastAPI(
    title="Zapier API",
    description="API for interfacing with Zapier to execute actions and list available actions.",
)

api_key_header = APIKeyHeader(name='Api-key', auto_error=True, scheme_name='api-key')
oauth_token_header = APIKeyHeader(name='Oauth-Token', auto_error=True, scheme_name='oauth-token')


class ApiKeys(BaseModel):
    api_key: str
    oauth_token: str


class ExecuteActionRequest(BaseModel):
    instructions: str = Field(..., description='Natural language instructions for the action')


async def get_api_key(api_key: str = Depends(api_key_header), oauth_token: str = Depends(oauth_token_header)):
    if not api_key and not oauth_token:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return ApiKeys(api_key=api_key, oauth_token=oauth_token)


@app.get('/actions/list', summary='List Available Zapier Actions', tags=['Zapier'])
async def list_zapier_actions(api_keys: ApiKeys = Depends(get_api_key)):
    try:
        if api_keys.api_key:
            tool_spec = ZapierToolSpec(api_key=api_keys.api_key)
        else:
            tool_spec = ZapierToolSpec(oauth_access_token=api_keys.oauth_token)
        actions = tool_spec.list_actions()
        return actions
    except Exception as e:
        return {"error": str(e)}


@app.post('/actions/execute/{action_id}', summary='Execute a Zapier Action by ID', tags=['Zapier'])
async def execute_zapier_action(action_id: str, execute_request: ExecuteActionRequest,
                                api_keys: ApiKeys = Depends(get_api_key), ):
    try:
        if api_keys.api_key:
            tool_spec = ZapierToolSpec(api_key=api_keys.api_key)
        else:
            tool_spec = ZapierToolSpec(oauth_access_token=api_keys.oauth_token)
        result = tool_spec.natural_language_query(id=action_id, instructions=execute_request.instructions)
        return result
    except Exception as e:
        return {"error": str(e)}
