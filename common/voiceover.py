import asyncio
import os
import edge_tts

# A distinct voice per channel so they don't all sound identical
VOICES = {
    "geology": "en-US-GuyNeural",
    "cosmology": "en-US-AriaNeural",
    "facts": "en-GB-RyanNeural",
    "funny": "en-US-JennyNeural",
}


async def _generate(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_voiceover(text, channel_key, output_path="output/voice.mp3"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    voice = VOICES.get(channel_key, "en-US-AriaNeural")
    asyncio.run(_generate(text, voice, output_path))
    return output_path
