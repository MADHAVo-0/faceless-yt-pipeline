import requests

CHANNEL_KEY = "funny"
VOICE_PROMPT = (
    "You are writing for an energetic, funny 'Top moments' YouTube Shorts "
    "channel. Narrate and describe the moment in words and stats only - "
    "never reference showing actual video footage, since none is used."
)


def get_topic():
    r = requests.get(
        "https://www.reddit.com/r/nextfuckinglevel/top.json",
        params={"limit": 5, "t": "day"},
        headers={"User-Agent": "faceless-yt-pipeline/1.0"},
    )
    r.raise_for_status()
    posts = r.json()["data"]["children"]
    if not posts:
        raise RuntimeError("No posts found today")
    post = posts[0]["data"]
    return {
        "id": post["id"],
        "title": post["title"],
        "summary": post["title"],
        "image_query": "amazing moment energetic action",
    }
