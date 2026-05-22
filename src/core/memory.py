from src.config.settings import settings
import tiktoken
from google import genai
from google.genai import types

class ConversationMemory:
    def __init__(self):
        self.summary = ""
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Cocok untuk Gemini

    def count_tokens(self, text: str) -> int:
        """Hitung jumlah token"""
        return len(self.tokenizer.encode(text))

    def summarize_conversation(self, history: list) -> str:
        """Buat ringkasan percakapan jika terlalu panjang"""
        if len(history) < 6:  # Terlalu pendek, tidak perlu summary
            return self.summary

        # Gabungkan history jadi teks
        conversation_text = "\n".join([
            f"User: {msg['parts'][0]['text']}" if msg['role'] == 'user' else f"EmpathAI: {msg['parts'][0]['text']}"
            for msg in history[-10:]  # Ambil 10 pesan terakhir
        ])

        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            prompt = f"""
            Buatlah ringkasan singkat dan jelas dari percakapan berikut. 
            Fokus pada perasaan user, topik utama, dan hal penting yang dibahas.
            Ringkasan harus netral dan empati.

            Percakapan:
            {conversation_text}

            Ringkasan:
            """

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=300
                )
            )
            
            new_summary = response.text.strip()
            self.summary = new_summary
            return new_summary

        except:
            return self.summary