from fastapi.security import APIKeyHeader
from llama_hub.tools.slack import SlackToolSpec
from fastapi import FastAPI, Query, Security, HTTPException
from typing import List, Union

from pydantic import BaseModel, Field

app = FastAPI(title="Slack API", description="API for interacting with Slack for various operations.")

app = FastAPI()

api_key_header = APIKeyHeader(name='Slack-Token', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


class SendMessageRequest(BaseModel):
    channel_id: str = Field(..., description='Channel ID to send a message to'),
    message: str = Field(..., description='The message to send'),


@app.get('/slack/load_data', summary='Load messages from Slack channels', tags=['Slack'])
async def load_data(
        channel_ids: List[str] = Query(..., description='List of channel IDs to fetch messages from'),
        reverse_chronological: bool = Query(True, description='Load messages in reverse chronological order'),
        slack_token: str = Security(get_api_key),
) -> Union[str, dict]:
    tool_spec = SlackToolSpec(slack_token=slack_token)

    try:
        data = tool_spec.load_data(channel_ids, reverse_chronological)
        return data.model_dump_json()
    except Exception as e:
        return {"error": str(e)}


@app.post('/slack/send_message', summary='Send a message to a Slack channel', tags=['Slack'])
async def send_message(
        send_message_request: SendMessageRequest,
        slack_token: str = Security(get_api_key),
) -> dict:
    tool_spec = SlackToolSpec(slack_token=slack_token)

    try:
        tool_spec.send_message(send_message_request.channel_id, send_message_request.message)
        return {'result': 'Message sent successfully'}
    except Exception as e:
        return {"error": str(e)}


@app.get('/slack/fetch_channels', summary='Fetch list of Slack channels', tags=['Slack'])
async def fetch_channels(
        slack_token: str = Security(get_api_key),
) -> Union[str, dict]:
    tool_spec = SlackToolSpec(slack_token=slack_token)

    try:
        channels_output = tool_spec.fetch_channels()
        return channels_output.model_dump_json()
    except Exception as e:
        return {"error": str(e)}
