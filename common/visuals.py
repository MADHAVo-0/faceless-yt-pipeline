import os
import requests

PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
PIXABAY_KEY = os.environ.get("PIXABAY_API_KEY")


def fetch_images(query, count=5):
    """Pixabay first - key issuance is always open there. Pexels is only
    tried as a bonus if a working key happens to be set."""
    images = []
    if PIXABAY_KEY:
        try:
            images = fetch_pixabay_images(query, count)
        except requests.exceptions.RequestException:
            images = []
    if not images and PEXELS_KEY:
        try:
            images = fetch_pexels_images(query, count)
        except requests.exceptions.RequestException:
            images = []
    if not images:
        raise RuntimeError(f"No images found for query: {query}")
    return images


def fetch_pexels_images(query, count=5):
    headers = {"Authorization": PEXELS_KEY}
    r = requests.get(
        "https://api.pexels.com/v1/search",
        params={"query": query, "per_page": count, "orientation": "portrait"},
        headers=headers,
    )
    r.raise_for_status()
    return [p["src"]["large"] for p in r.json().get("photos", [])]


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
