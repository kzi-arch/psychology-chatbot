from datetime import datetime, timedelta
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 20, time_window: int = 60):
        self.max_requests = max_requests      # Maksimal request per user
        self.time_window = time_window        # Dalam detik
        self.user_requests = defaultdict(list)

    def can_make_request(self, user_id: str = "default") -> tuple[bool, str]:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)

        # Bersihkan request lama
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id] 
            if req_time > cutoff
        ]

        if len(self.user_requests[user_id]) >= self.max_requests:
            wait_time = int((self.user_requests[user_id][0] + timedelta(seconds=self.time_window) - now).total_seconds())
            return False, f"Terlalu banyak pesan. Tunggu {wait_time} detik lagi ya."

        # Tambah request baru
        self.user_requests[user_id].append(now)
        return True, ""