import json
import os
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL_CANDIDATES = ["gemini-flash-latest", "gemini-flash-lite-latest"]


def generate_script(topic_title, topic_summary, channel_prompt, max_retries=3):
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
    last_error = None
    for model_name in MODEL_CANDIDATES:
        delay = 15
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                return json.loads(response.text)
            except ServerError as e:
                last_error = e
                if attempt == max_retries:
                    print(f"{model_name} still unavailable after {max_retries} tries, trying next model...")
                    break
                print(f"{model_name} busy (attempt {attempt}/{max_retries}), waiting {delay}s...")
                time.sleep(delay)
                delay *= 2
            except ClientError as e:
                last_error = e
                if getattr(e, "code", None) == 429:
                    print("Rate limit hit (429) - waiting 60s for the window to reset...")
                    time.sleep(60)
                    continue
                raise  # other client errors (bad key, bad request) shouldn't be retried
    raise last_error
