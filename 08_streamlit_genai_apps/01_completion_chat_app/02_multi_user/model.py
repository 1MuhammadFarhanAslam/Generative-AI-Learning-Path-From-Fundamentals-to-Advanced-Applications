import os
import uuid
import json
from datetime import datetime
from typing import List, Dict

# ✅ Persistent directory for all user chats
BASE_CHAT_DIR = "chats"

def _get_user_chat_dir(user_id: str) -> str:
    user_dir = os.path.join(BASE_CHAT_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def create_new_chat(user_id: str, title: str = "New Chat") -> str:
    user_dir = _get_user_chat_dir(user_id)
    chat_id = str(uuid.uuid4())
    chat_file_path = os.path.join(user_dir, f"{chat_id}.json")

    chat_data = {
        "id": chat_id,
        "user_id": user_id,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }

    with open(chat_file_path, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2)

    return chat_id

def list_chat_ids_for_user(user_id: str) -> List[str]:
    user_dir = _get_user_chat_dir(user_id)
    return [f.split(".")[0] for f in os.listdir(user_dir) if f.endswith(".json")]

def list_chats_for_user(user_id: str) -> List[Dict]:
    user_dir = _get_user_chat_dir(user_id)
    chats = []
    for fname in os.listdir(user_dir):
        if fname.endswith(".json"):
            with open(os.path.join(user_dir, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                chats.append({
                    "id": data["id"],
                    "title": data["title"],
                    "created_at": data["created_at"]
                })
    # Sort chats by created_at descending
    return sorted(chats, key=lambda x: x["created_at"], reverse=True)

def get_chat_by_id(user_id: str, chat_id: str) -> Dict:
    chat_path = os.path.join(_get_user_chat_dir(user_id), f"{chat_id}.json")
    if not os.path.exists(chat_path):
        return None
    with open(chat_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_chat_by_id(user_id: str, chat_id: str, chat_data: Dict) -> None:
    chat_path = os.path.join(_get_user_chat_dir(user_id), f"{chat_id}.json")
    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2)

def rename_chat_title(user_id: str, chat_id: str, new_title: str) -> None:
    chat = get_chat_by_id(user_id, chat_id)
    if chat:
        chat["title"] = new_title
        save_chat_by_id(user_id, chat_id, chat)

def delete_chat_by_id(user_id: str, chat_id: str) -> None:
    chat_path = os.path.join(_get_user_chat_dir(user_id), f"{chat_id}.json")
    if os.path.exists(chat_path):
        os.remove(chat_path)


# --- BotModel: Handles reply generation using OpenAI ---

import openai

class BotModel:
    def __init__(self, model="gpt-3.5-turbo", api_key=None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("⚠️ Warning: OPENAI_API_KEY not set. Running in mock mode.")
        else:
            openai.api_key = self.api_key

    def generate_reply(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a reply based on chat history.
        If OpenAI API key is set, use GPT. Otherwise, return echo.
        """
        if not messages:
            return "Hello! How can I assist you today?"

        if not self.api_key:
            # Mock mode fallback
            last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
            return f"Echo: {last_user_msg}"

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            print(f"❌ OpenAI API Error: {e}")
            return "Sorry, I'm having trouble generating a response right now."
