import os
import requests

PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
PIXABAY_KEY = os.environ.get("PIXABAY_API_KEY")


def fetch_pexels_images(query, count=5):
    headers = {"Authorization": PEXELS_KEY}
    r = requests.get(
        "https://api.pexels.com/v1/search",
        params={"query": query, "per_page": count, "orientation": "portrait"},
        headers=headers,
    )
    r.raise_for_status()
    photos = r.json().get("photos", [])
    if not photos:
        # fall back to Pixabay if Pexels has nothing for this query
        return fetch_pixabay_images(query, count)
    return [p["src"]["large"] for p in photos]


def fetch_pixabay_images(query, count=5):
    r = requests.get(
        "https://pixabay.com/api/",
        params={"key": PIXABAY_KEY, "q": query, "per_page": count, "image_type": "photo"},
    )
    r.raise_for_status()
    return [h["largeImageURL"] for h in r.json().get("hits", [])]


def download_images(urls, folder="output/images"):
    os.makedirs(folder, exist_ok=True)
    paths = []
    for i, url in enumerate(urls):
        path = f"{folder}/img_{i}.jpg"
        r = requests.get(url)
        with open(path, "wb") as f:
            f.write(r.content)
        paths.append(path)
    return paths
