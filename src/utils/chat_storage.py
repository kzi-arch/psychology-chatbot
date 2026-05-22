import json
import os
from datetime import datetime
from pathlib import Path
from src.utils.feedback import FeedbackManager

class ChatStorage:
    def __init__(self):
        self.data_dir = Path("data/conversations")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_manager = FeedbackManager()   # ← Tambahkan ini

    def save_chat(self, messages: list, title: str = None) -> str:
        """Simpan chat ke file JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not title:
            title = f"Chat_{timestamp}"
        
        filename = f"{timestamp}_{title.replace(' ', '_')[:30]}.json"
        filepath = self.data_dir / filename

        chat_data = {
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "messages": messages
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(chat_data, f, ensure_ascii=False, indent=2)

        return str(filepath)

    def load_chat(self, filename: str) -> dict:
        """Load chat dari file"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def list_chats(self) -> list:
        """Daftar semua chat yang tersimpan"""
        chats = []
        for file in self.data_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    chats.append({
                        "filename": file.name,
                        "title": data.get("title", "Untitled"),
                        "timestamp": data.get("timestamp"),
                        "message_count": len(data.get("messages", []))
                    })
            except:
                continue
        
        # Urutkan berdasarkan waktu (terbaru di atas)
        chats.sort(key=lambda x: x["timestamp"], reverse=True)
        return chats