import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv


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

    return extracted_data


load_dotenv()

api_endpoint = "https://draft.premierleague.com/api/bootstrap-static"
event_data = fetch_event_data(api_endpoint)
for gw, dt in event_data:
    print(gw, dt)
