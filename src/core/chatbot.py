from google import genai
from google.genai import types
from src.config.settings import settings
from src.config.prompts import PERSONAS, SAFETY_REMINDER, RAG_PROMPT_TEMPLATE
from src.core.safety import SafetyGuard
from src.core.memory import ConversationMemory
from src.psychology.knowledge_base import PsychologyKnowledgeBase
from src.utils.logging import AppLogger
from src.core.rate_limiter import RateLimiter

class PsychologyChatbot:
    def __init__(self, persona_key: str = "empat"):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.safety = SafetyGuard()
        self.memory = ConversationMemory()
        self.knowledge_base = PsychologyKnowledgeBase()
        self.logger = AppLogger()
        self.rate_limiter = RateLimiter(max_requests=15, time_window=60)  # 15 pesan per menit
        self.current_persona = persona_key
        self.history = []

    def set_persona(self, persona_key: str):
        """Ganti persona"""
        if persona_key in PERSONAS:
            self.current_persona = persona_key
            self.history = []  # Reset history saat ganti persona
            self.memory.summary = ""
            return True
        return False

    def clear_history(self):
        """Hapus riwayat percakapan dan ringkasan memori"""
        self.history = []
        self.memory.summary = ""

    def get_response(self, user_message: str, user_id: str = "default") -> str:
        # Rate Limiting Check
        can_proceed, limit_message = self.rate_limiter.can_make_request(user_id)
        if not can_proceed:
            return limit_message

        # Safety Check
        is_safe, safety_message = self.safety.get_safety_response(user_message)
        if not is_safe:
            return safety_message

        # RAG Retrieval
        retrieved_docs = self.knowledge_base.retrieve(user_message, k=settings.RAG_K)
        context = "\n\n---\n\n".join(retrieved_docs) if retrieved_docs else ""

        # Persona Prompt
        persona_info = PERSONAS[self.current_persona]
        persona_prompt = persona_info["prompt"]
        persona_name = persona_info["name"]

        system_instruction = f"""{persona_prompt}

PENTING: Kamu saat ini sedang berperan sebagai persona "{persona_name}".
Pastikan gaya bahasa, nada bicara, dan pendekatanmu BENAR-BENAR mencerminkan persona ini dari awal sampai akhir!

{SAFETY_REMINDER}

{RAG_PROMPT_TEMPLATE.format(context=context) if context else ""}
"""

        if self.memory.summary:
            system_instruction += f"\n\nRingkasan percakapan: {self.memory.summary}"

        self.history.append({"role": "user", "parts": [{"text": user_message}]})

        try:
            # Log interaksi
            self.logger.log_interaction(
                user_id=user_id,
                action="generate_response",
                details={
                    "persona": self.current_persona,
                    "message_length": len(user_message),
                    "history_length": len(self.history)
                }
            )

            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=self.history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_TOKENS,
                )
            )

            bot_reply = response.text.strip()
            self.history.append({"role": "model", "parts": [{"text": bot_reply}]})

            if len(self.history) > 10:
                self.memory.summarize_conversation(self.history)

            return bot_reply

        except Exception as e:
            self.logger.log_error(e, context="generate_content")
            return "Maaf, sedang ada gangguan. Coba lagi sebentar ya."