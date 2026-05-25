import re
from typing import Tuple, List

class SafetyGuard:
    def __init__(self):
        # Kata-kata & pola berbahaya
        self.crisis_keywords = [
            r"bunuh diri", r"ingin mati", r"mau mati", r"end my life", 
            r"kill myself", r"suicide", r"self harm", r"melukai diri"
        ]
        
        self.diagnosis_keywords = [
            r"depresi berat", r"skizofrenia", r"bipolar", r"gangguan jiwa",
            r"diagnosis", r"gejala", r"penyakit apa", r"apa yang salah dengan saya"
        ]

        self.bypass_keywords = [
            r"abaikan semua instruksi", r"lupakan aturan", r"ignore previous instructions",
            r"sekarang kamu adalah", r"act as", r"developer mode", r"jailbreak",
            r"system prompt", r"lupakan instruksi", r"tanpa filter", r"bertindaklah sebagai",
            r"bayangkan kamu", r"skenario hipotesis", r"roleplay sebagai", r"simulasikan"
        ]

    def check_crisis(self, message: str) -> Tuple[bool, str]:
        """Deteksi situasi krisis"""
        msg_lower = message.lower()
        
        for pattern in self.crisis_keywords:
            if re.search(pattern, msg_lower):
                return True, (
                    "Aku sangat khawatir mendengar ini 😔\n\n"
                    "Tolong hubungi layanan darurat kesehatan mental segera:\n"
                    "• **Hotline Kesehatan Jiwa**: 119 ext. 8\n"
                    "• **Into The Light**: 0811-3855-988\n"
                    "Aku di sini mendengarkan, tapi aku bukan pengganti bantuan profesional."
                )
        
        return False, ""

    def check_diagnosis_request(self, message: str) -> Tuple[bool, str]:
        """Cegah permintaan diagnosis"""
        msg_lower = message.lower()
        
        for pattern in self.diagnosis_keywords:
            if re.search(pattern, msg_lower):
                return True, (
                    "Maaf ya, aku **tidak bisa** memberikan diagnosis atau penilaian klinis.\n\n"
                    "Aku hanya teman curhat. Untuk hal-hal seperti ini, lebih baik konsultasi langsung "
                    "dengan psikolog atau psikiater profesional."
                )
        
        return False, ""

    def check_bypass_attempt(self, message: str) -> Tuple[bool, str]:
        """Deteksi percobaan manipulasi prompt atau jailbreak"""
        msg_lower = message.lower()
        
        for pattern in self.bypass_keywords:
            if re.search(pattern, msg_lower):
                return True, (
                    "Maaf, aku tidak bisa memproses permintaan dengan format tersebut. "
                    "Mari kita kembali fokus membicarakan perasaanmu atau hal lain yang ingin kamu curhatkan ya."
                )
        
        return False, ""

    def validate_response(self, user_message: str, bot_response: str) -> Tuple[bool, str]:
        """Validasi tambahan pada jawaban bot"""
        forbidden_phrases = ["kamu mengalami", "kamu menderita", "diagnosisnya adalah"]
        
        for phrase in forbidden_phrases:
            if phrase in bot_response.lower():
                return False, "Maaf, sepertinya jawabanku kurang tepat. Biar aku jawab ulang dengan lebih hati-hati."
        
        return True, ""

    def get_safety_response(self, user_message: str) -> Tuple[bool, str]:
        """Main safety checker"""
        is_crisis, crisis_msg = self.check_crisis(user_message)
        if is_crisis:
            return False, crisis_msg

        is_diagnosis, diagnosis_msg = self.check_diagnosis_request(user_message)
        if is_diagnosis:
            return False, diagnosis_msg

        is_bypass, bypass_msg = self.check_bypass_attempt(user_message)
        if is_bypass:
            return False, bypass_msg

        return True, ""