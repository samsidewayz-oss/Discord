import os
import sys
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# Validate required environment variables
REQUIRED_SECRETS = {
    'GOOGLE_REFRESH_TOKEN': 'Google Refresh Token',
    'GOOGLE_CLIENT_ID': 'Google Client ID',
    'GOOGLE_CLIENT_SECRET': 'Google Client Secret',
    'DISCORD_WEBHOOK': 'Discord Webhook URL'
}

missing_secrets = [name for name in REQUIRED_SECRETS.keys() if not os.getenv(name)]
if missing_secrets:
    print(f"Error: Missing required environment variables: {', '.join(missing_secrets)}")
    sys.exit(1)

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# Validate Discord webhook is a valid URL
if not DISCORD_WEBHOOK.startswith('https://'):
    print("Error: DISCORD_WEBHOOK must be a valid HTTPS URL")
    sys.exit(1)

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
    response = requests.post(
        DISCORD_WEBHOOK,
        json={"content": message}
    )
    response.raise_for_status()


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
