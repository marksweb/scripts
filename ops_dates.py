import os

import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def fetch_event_data(api_url: str) -> list[tuple[str, str]]:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    events = data["events"]["data"]
    extracted_data = [
        (
            event["name"],
            (
                datetime.strptime(event["trades_time"], "%Y-%m-%dT%H:%M:%SZ")
                - timedelta(days=2)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        for event in events
    ]

    create_google_calendar_events(extracted_data)
    return extracted_data


def create_google_calendar_events(events: list[tuple[str, str]]) -> None:
    """TODO check if entry exists before creating?"""
    credentials = Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    service = build("calendar", "v3", credentials=credentials)
    for name, trades_time in events:
        event = {
            "summary": name,
            "start": {"dateTime": trades_time, "timeZone": "UTC"},
            "end": {
                "dateTime": trades_time,
                "timeZone": "UTC",
            },  # Assuming all-day event
        }
        service.events().insert(calendarId="primary", body=event).execute()


load_dotenv()

api_endpoint = "https://draft.premierleague.com/api/bootstrap-static"
event_data = fetch_event_data(api_endpoint)
print(event_data)
