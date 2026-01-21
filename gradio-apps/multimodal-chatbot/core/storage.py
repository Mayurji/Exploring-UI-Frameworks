import json
from pathlib import Path

CHAT_PATH = Path("data/chats/chat_history.json")
CHAT_PATH.parent.mkdir(parents=True, exist_ok=True)

def save_chat(history):
    with open(CHAT_PATH, "w") as f:
        json.dump(history, f, indent=2)

def load_chat():
    if CHAT_PATH.exists():
        try:
            with open(CHAT_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []
