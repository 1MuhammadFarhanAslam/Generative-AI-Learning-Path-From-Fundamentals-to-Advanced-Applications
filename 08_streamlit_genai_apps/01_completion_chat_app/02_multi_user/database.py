import os
import json
from typing import List, Dict

class Database:
    def __init__(self, db_root: str = "chat_data") -> None:
        self.db_root = db_root
        os.makedirs(self.db_root, exist_ok=True)

    def _get_user_dir(self, user_id: str) -> str:
        path = os.path.join(self.db_root, user_id)
        os.makedirs(path, exist_ok=True)
        return path

    def _get_chat_file(self, user_id: str, chat_id: str) -> str:
        return os.path.join(self._get_user_dir(user_id), f"{chat_id}.json")

    def _get_meta_file(self, user_id: str) -> str:
        return os.path.join(self._get_user_dir(user_id), "meta.json")

    def load_chat_history(self, user_id: str, chat_id: str) -> List[dict]:
        file_path = self._get_chat_file(user_id, chat_id)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_chat_history(self, user_id: str, chat_id: str, messages: List[dict]):
        file_path = self._get_chat_file(user_id, chat_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

    def delete_chat(self, user_id: str, chat_id: str):
        file_path = self._get_chat_file(user_id, chat_id)
        if os.path.exists(file_path):
            os.remove(file_path)
        meta = self._load_meta(user_id)
        if chat_id in meta:
            del meta[chat_id]
            self._save_meta(user_id, meta)

    def _load_meta(self, user_id: str) -> Dict[str, str]:
        meta_path = self._get_meta_file(user_id)
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_meta(self, user_id: str, meta: Dict[str, str]):
        meta_path = self._get_meta_file(user_id)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    def save_chat_title_if_new(self, user_id: str, chat_id: str, title: str):
        meta = self._load_meta(user_id)
        if chat_id not in meta:
            meta[chat_id] = title
            self._save_meta(user_id, meta)

    def rename_chat(self, user_id: str, chat_id: str, new_title: str):
        meta = self._load_meta(user_id)
        if chat_id in meta:
            meta[chat_id] = new_title
            self._save_meta(user_id, meta)

    def list_chats(self, user_id: str) -> Dict[str, str]:
        return self._load_meta(user_id)
