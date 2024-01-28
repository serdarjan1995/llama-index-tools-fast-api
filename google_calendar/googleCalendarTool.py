from fastapi import FastAPI, Depends, HTTPException
from llama_hub.tools.google_calendar import GoogleCalendarToolSpec
from typing import List, Optional
from datetime import datetime

app = FastAPI()


def get_google_calendar_tool_spec(api_key: str = Depends(oauth2_scheme)):
    return GoogleCalendarToolSpec(api_key=api_key)


@app.get('/load-data', summary='Load data from users calendar')
def load_data(number_of_results: Optional[int] = 100, start_date: Optional[str] = None,
              api_key: str = Depends(oauth2_scheme)):
    tool = get_google_calendar_tool_spec(api_key)
    return tool.load_data(number_of_results=number_of_results, start_date=start_date)


@app.post('/create-event', summary='Create an event on the users calendar')
def create_event(title: Optional[str] = None, description: Optional[str] = None, location: Optional[str] = None,
                 start_datetime: Optional[str] = None, end_datetime: Optional[str] = None,
                 attendees: Optional[List[str]] = None, api_key: str = Depends(oauth2_scheme)):
    tool = get_google_calendar_tool_spec(api_key)
    return tool.create_event(title=title, description=description, location=location, start_datetime=start_datetime,
                             end_datetime=end_datetime, attendees=attendees)


@app.get('/get-date', summary='Get the current date')
def get_date(api_key: str = Depends(oauth2_scheme)):
    tool = get_google_calendar_tool_spec(api_key)
    return tool.get_date()
