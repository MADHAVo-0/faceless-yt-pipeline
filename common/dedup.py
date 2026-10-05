
import json
import os

DEDUP_FILE = "data/used_topics.json"


def load_used_topics():
    if not os.path.exists(DEDUP_FILE):
        return {}
    with open(DEDUP_FILE, "r") as f:
        return json.load(f)


def is_used(channel, topic_id):
    data = load_used_topics()
    return topic_id in data.get(channel, [])


def mark_used(channel, topic_id):
    data = load_used_topics()
    data.setdefault(channel, [])
    if topic_id not in data[channel]:
        data[channel].append(topic_id)
    with open(DEDUP_FILE, "w") as f:
        json.dump(data, f, indent=2)
