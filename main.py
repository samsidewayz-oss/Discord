import os
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_calendar_events():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=SCOPES
    )

    service = build("calendar", "v3", credentials=creds)

    today = datetime.utcnow().date()

    start = datetime.combine(today, datetime.min.time()).isoformat() + "Z"
    end = datetime.combine(today, datetime.max.time()).isoformat() + "Z"

    events = service.events().list(
        calendarId="primary",
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events.get("items", [])


def send_discord(message):
    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message}
    )


def main():
    events = get_calendar_events()

    today = datetime.now().strftime("%A %d %B")

    message = f"☀️ **SIDEWAYZ Daily Assistant**\n\n📅 {today}\n\n"

    if not events:
        message += "No calendar events today. Clear schedule 🔥"
    else:
        message += "**Today's Schedule:**\n"

        for event in events:
            start = event["start"].get(
                "dateTime",
                "All day"
            )

            summary = event.get(
                "summary",
                "Untitled"
            )

            message += f"• {start} — {summary}\n"

    send_discord(message)


if __name__ == "__main__":
    main()
