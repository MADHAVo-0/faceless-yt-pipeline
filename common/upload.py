import os
import google.oauth2.credentials
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload


def upload_video(video_path, title, description, channel_key):
    creds = google.oauth2.credentials.Credentials(
        None,
        refresh_token=os.environ[f"{channel_key.upper()}_YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {"title": title, "description": description, "categoryId": "27"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    return response["id"]
