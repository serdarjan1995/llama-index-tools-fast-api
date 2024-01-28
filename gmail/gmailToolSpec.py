from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from llama_hub.tools.gmail import GmailToolSpec

app = FastAPI(title='Gmail Tool API')

tool_spec = GmailToolSpec()


class Email(BaseModel):
    to: List[EmailStr]
    subject: str
    body: str


@app.get('/email/load', summary='Load Recent Emails')
def load_recent_emails(q: Optional[str] = '', max_results: Optional[int] = 10):
    try:
        emails = tool_spec.search_messages(query=q, max_results=max_results)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/email/draft', summary='Create Email Draft')
def create_email_draft(email: Email):
    draft = tool_spec.create_draft(
        to=email.to,
        subject=email.subject,
        message=email.body
    )
    return {'draft_id': draft['id']}


@app.put('/email/draft/{draft_id}', summary='Update Email Draft')
def update_email_draft(draft_id: str, email: Email):
    updated_draft = tool_spec.update_draft(
        draft_id=draft_id,
        to=email.to,
        subject=email.subject,
        message=email.body
    )
    return {'updated_draft_id': updated_draft['id']}


@app.get('/email/draft/{draft_id}', summary='Get Email Draft')
def get_email_draft(draft_id: str):
    draft = tool_spec.get_draft(draft_id=draft_id)
    return draft


@app.post('/email/send', summary='Send Email Draft')
def send_email_draft(draft_id: str = Field(..., description='The draft ID to send')):
    sent_message = tool_spec.send_draft(draft_id=draft_id)
    return {'message_id': sent_message['id']}
