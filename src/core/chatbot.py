from google import genai
from google.genai import types
from src.config.settings import settings
from src.config.prompts import SYSTEM_PROMPT, SAFETY_REMINDER, RAG_PROMPT_TEMPLATE
from src.core.safety import SafetyGuard
from src.core.memory import ConversationMemory
from src.psychology.knowledge_base import PsychologyKnowledgeBase

class PsychologyChatbot:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.safety = SafetyGuard()
        self.memory = ConversationMemory()
        self.knowledge_base = PsychologyKnowledgeBase()
        self.history = []

    def get_response(self, user_message: str) -> str:
        # Safety Check
        is_safe, safety_message = self.safety.get_safety_response(user_message)
        if not is_safe:
            return safety_message

        # Retrieve knowledge
        retrieved_docs = self.knowledge_base.retrieve(user_message, k=4)
        context = "\n\n---\n\n".join(retrieved_docs) if retrieved_docs else "Tidak ada konteks tambahan."

        # Tambah ke history
        self.history.append({"role": "user", "parts": [{"text": user_message}]})

        # Bangun system instruction
        system_instruction = f"""{SYSTEM_PROMPT}
{SAFETY_REMINDER}

{RAG_PROMPT_TEMPLATE.format(context=context)}
"""

        if self.memory.summary:
            system_instruction += f"\n\nRingkasan percakapan sebelumnya:\n{self.memory.summary}"

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=self.history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_TOKENS,
                )
            )

            bot_reply = response.text

            self.history.append({"role": "model", "parts": [{"text": bot_reply}]})

            # Auto summary
            if len(self.history) > 12:
                self.memory.summarize_conversation(self.history)

            return bot_reply

        except Exception as e:
            print(f"Error memanggil Gemini API: {e}")
            return "Maaf, aku sedang mengalami gangguan. Coba lagi ya? 😊"