import json
import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# "gemini-flash-latest" always points at Google's current free-tier Flash
# model, so this keeps working even after Google retires a specific version.
MODEL_NAME = "gemini-flash-latest"


def generate_script(topic_title, topic_summary, channel_prompt):
    model = genai.GenerativeModel(MODEL_NAME)
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
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)
