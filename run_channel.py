import sys
import os
import importlib

from common.dedup import is_used, mark_used
from common.script_gen import generate_script
from common.voiceover import generate_voiceover
from common.visuals import fetch_images, download_images
from common.assemble import assemble_video
from common.upload import upload_video


def main(channel_name):
    channel = importlib.import_module(f"channels.{channel_name}")
    topic = channel.get_topic()

    if is_used(channel.CHANNEL_KEY, topic["id"]):
        print(f"Topic '{topic['id']}' already used for {channel_name}, skipping today.")
        return

    result = generate_script(topic["title"], topic["summary"], channel.VOICE_PROMPT)

    os.makedirs("output", exist_ok=True)
    audio_path = generate_voiceover(result["script"], channel.CHANNEL_KEY)

    image_urls = fetch_images(topic["image_query"], count=5)
    image_paths = download_images(image_urls)

    video_path = assemble_video(image_paths, audio_path)

    video_id = upload_video(video_path, result["title"], result["description"], channel.CHANNEL_KEY)
    print(f"Uploaded: https://youtube.com/watch?v={video_id}")

    mark_used(channel.CHANNEL_KEY, topic["id"])


if __name__ == "__main__":
    main(sys.argv[1])
