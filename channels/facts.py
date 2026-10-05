import datetime
import requests

CHANNEL_KEY = "facts"
VOICE_PROMPT = (
    "You are writing for a punchy, surprising 'did you know' YouTube Shorts "
    "channel about facts most people don't know."
)


def get_topic():
    today = datetime.datetime.utcnow()
    r = requests.get(
        f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{today.month:02d}/{today.day:02d}"
    )
    r.raise_for_status()
    events = r.json().get("events", [])
    if not events:
        raise RuntimeError("No events found for today")
    event = events[0]
    return {
        "id": f"{today.month}-{today.day}-{event.get('year')}",
        "title": f"On this day, {event.get('year')}",
        "summary": event["text"],
        "image_query": "history interesting fact",
    }
