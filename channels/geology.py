import requests

CHANNEL_KEY = "geology"
VOICE_PROMPT = (
    "You are writing for a dramatic, awe-struck YouTube Shorts channel "
    "about Earth's geology and natural events."
)


def get_topic():
    r = requests.get(
        "https://eonet.gsfc.nasa.gov/api/v3/events",
        params={"status": "open", "limit": 5},
    )
    r.raise_for_status()
    events = r.json().get("events", [])
    if not events:
        raise RuntimeError("No open natural events found today")
    event = events[0]
    category = event["categories"][0]["title"]
    return {
        "id": event["id"],
        "title": event["title"],
        "summary": f"Category: {category}",
        "image_query": f"{category} nature landscape",
    }
