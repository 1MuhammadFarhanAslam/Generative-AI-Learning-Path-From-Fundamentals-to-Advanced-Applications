import os
import json

SESSION_DIR = "session_state"
BASE_CHAT_DIR = "chats"

def get_user_session_path(user_id):
    return os.path.join(SESSION_DIR, f"{user_id}.json")

def save_user_session_state(user_id, state_dict):
    os.makedirs(SESSION_DIR, exist_ok=True)
    with open(get_user_session_path(user_id), "w") as f:
        json.dump(state_dict, f)

def load_user_session_state(user_id):
    try:
        with open(get_user_session_path(user_id), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
