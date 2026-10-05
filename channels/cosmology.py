import os
import requests

CHANNEL_KEY = "cosmology"
VOICE_PROMPT = (
    "You are writing for a calm, documentary-style YouTube Shorts channel "
    "about space and cosmology."
)


def get_topic():
    key = os.environ.get("NASA_API_KEY", "DEMO_KEY")
    r = requests.get("https://api.nasa.gov/planetary/apod", params={"api_key": key})
    r.raise_for_status()
    data = r.json()
    return {
        "id": data["date"],
        "title": data["title"],
        "summary": data.get("explanation", "")[:600],
        "image_query": "space nebula galaxy astronomy",
    }
