import json
import os
from datetime import datetime
from pathlib import Path

class FeedbackManager:
    def __init__(self):
        self.feedback_dir = Path("data/feedback")
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.feedback_dir / "feedback_log.jsonl"

    def save_feedback(self, message_index: int, user_message: str, bot_response: str, 
                     rating: int, comment: str = ""):
        """Simpan feedback"""
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "message_index": message_index,
            "user_message": user_message,
            "bot_response": bot_response,
            "rating": rating,           # 1 = Like, 0 = Dislike
            "comment": comment,
            "persona": "default"        # nanti bisa ditambah
        }

        with open(self.feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_data, ensure_ascii=False) + "\n")

    def get_total_feedback(self):
        """Hitung total feedback"""
        if not self.feedback_file.exists():
            return 0
        with open(self.feedback_file, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)