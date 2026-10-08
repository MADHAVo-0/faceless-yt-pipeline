import json
import os
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL_NAME = "gemini-flash-latest"


def generate_script(topic_title, topic_summary, channel_prompt, max_retries=4):
    prompt = f"""{channel_prompt}

Topic: {topic_title}
Background: {topic_summary}

Write all three of the following for a YouTube Short:
1. "script": the spoken narration only, 45-60 seconds when read aloud, no stage directions
2. "title": a catchy YouTube title, under 70 characters
3. "description": 2-3 sentences plus 3 relevant hashtags

Respond with ONLY valid JSON in this exact shape, nothing else:
{{"script": "...", "title": "...", "description": "..."}}
"""
    delay = 15
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            return json.loads(response.text)
        except ServerError:
            if attempt == max_retries:
                raise
            print(f"Gemini busy (attempt {attempt}/{max_retries}), waiting {delay}s...")
            time.sleep(delay)
            delay *= 2
