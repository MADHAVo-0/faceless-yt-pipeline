import os
import subprocess
from mutagen.mp3 import MP3


def get_audio_duration(path):
    return MP3(path).info.length


def assemble_video(image_paths, audio_path, output_path="output/final.mp4"):
    os.makedirs("output", exist_ok=True)
    duration = get_audio_duration(audio_path)
    per_image = max(duration / len(image_paths), 1)

    list_file = "output/images.txt"
    with open(list_file, "w") as f:
        for img in image_paths:
            f.write(f"file '{os.path.abspath(img)}'\n")
            f.write(f"duration {per_image}\n")
        f.write(f"file '{os.path.abspath(image_paths[-1])}'\n")

    slideshow_path = "output/slideshow.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
            "-vf",
            "scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-r", "30", slideshow_path,
        ],
        check=True,
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-i", slideshow_path, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest", output_path,
        ],
        check=True,
    )
    return output_path
