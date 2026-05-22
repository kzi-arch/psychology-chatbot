import sys
from pathlib import Path

# Tambahkan direktori root (satu tingkat di atas 'src') ke sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from src.core.chatbot import PsychologyChatbot
from src.config.settings import settings
from src.config.prompts import PERSONAS
from src.utils.chat_storage import ChatStorage
from src.utils.feedback import FeedbackManager
from datetime import datetime

# ====================== CONFIG ======================
st.set_page_config(
    page_title="EmpathAI - Teman Curhat",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Dark Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi
if "chatbot" not in st.session_state:
    st.session_state.chatbot = PsychologyChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_storage" not in st.session_state:
    st.session_state.chat_storage = ChatStorage()

if "feedback_manager" not in st.session_state:
    st.session_state.feedback_manager = FeedbackManager()

# ====================== SIDEBAR ======================
with st.sidebar:
    st.title("🧠 EmpathAI")
    st.caption("Teman Curhat Psikologi")

    # Persona Selector
    st.write("**Pilih Teman Curhat**")
    persona_options = {f"{p['emoji']} {p['name']}" : key for key, p in PERSONAS.items()}
    
    selected_persona_label = st.selectbox(
        "Persona",
        options=list(persona_options.keys()),
        index=0  # default = Empath
    )
    
    selected_persona_key = persona_options[selected_persona_label]

    # Update persona jika berubah
    if "current_persona" not in st.session_state or st.session_state.current_persona != selected_persona_key:
        st.session_state.current_persona = selected_persona_key
        if "chatbot" in st.session_state:
            st.session_state.chatbot.set_persona(selected_persona_key)
            st.session_state.messages = []  # Sinkronisasi: hapus chat di layar saat ganti persona
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Simpan Chat", type="primary", use_container_width=True):
            if st.session_state.messages:
                title = st.text_input("Judul Chat:", 
                                    value=f"Curhat {datetime.now().strftime('%d %B %Y')}", 
                                    key="save_title")
                if st.button("✅ Simpan"):
                    filepath = st.session_state.chat_storage.save_chat(
                        st.session_state.messages, title
                    )
                    st.success("Chat berhasil disimpan!")
            else:
                st.warning("Chat kosong.")

    with col2:
        if st.button("📤 Export ke TXT", type="secondary", use_container_width=True):
            if st.session_state.messages:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                filename = f"empathai_chat_{timestamp}.txt"
                
                chat_text = "=== EMPATHAI CHAT ===\n\n"
                for msg in st.session_state.messages:
                    role = "👤 Kamu" if msg["role"] == "user" else "🧠 EmpathAI"
                    chat_text += f"{role}:\n{msg['content']}\n\n"
                
                st.download_button(
                    label="⬇️ Download TXT",
                    data=chat_text,
                    file_name=filename,
                    mime="text/plain"
                )
            else:
                st.warning("Tidak ada chat untuk diekspor.")

    st.divider()

    if st.button("🗑️ Hapus Riwayat Chat", type="secondary"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_history()
        st.success("Riwayat dihapus.")

    # Saved Chats
    st.divider()
    st.write("**Chat Tersimpan**")
    saved_chats = st.session_state.chat_storage.list_chats()
    
    if saved_chats:
        for chat in saved_chats[:5]:
            if st.button(f"📜 {chat['title'][:30]}...", key=chat['filename']):
                loaded = st.session_state.chat_storage.load_chat(chat['filename'])
                if loaded:
                    st.session_state.messages = loaded['messages']
                    st.session_state.chatbot.history = []
                    st.rerun()
    else:
        st.caption("Belum ada chat tersimpan.")

    st.divider()
    st.caption(f"Model: {settings.GEMINI_MODEL}")

# ====================== MAIN CHAT ======================
st.title("💬 EmpathAI")
st.markdown("**Hai, aku di sini. Ceritakan apa yang kamu rasakan.**")

# Tampilkan pesan + Feedback
for idx, message in enumerate(st.session_state.messages):
    avatar = "👤" if message["role"] == "user" else "🧠"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        
        # Tambah feedback hanya untuk jawaban bot
        if message["role"] == "assistant" and idx > 0:
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("👍", key=f"like_{idx}"):
                    st.session_state.chat_storage.feedback_manager.save_feedback(
                        message_index=idx,
                        user_message=st.session_state.messages[idx-1]["content"],
                        bot_response=message["content"],
                        rating=1
                    )
                    st.success("Terima kasih atas feedbacknya!")
                    st.rerun()
            
            with col2:
                if st.button("👎", key=f"dislike_{idx}"):
                    comment = st.text_input("Kenapa tidak suka? (opsional)", 
                                          key=f"comment_{idx}")
                    if st.button("Kirim", key=f"submit_{idx}"):
                        st.session_state.chat_storage.feedback_manager.save_feedback(
                            message_index=idx,
                            user_message=st.session_state.messages[idx-1]["content"],
                            bot_response=message["content"],
                            rating=0,
                            comment=comment
                        )
                        st.success("Feedback diterima. Terima kasih!")
                        st.rerun()

# Input Chat
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("EmpathAI sedang mendengarkan..."):
            response = st.session_state.chatbot.get_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Refresh agar tombol feedback otomatis muncul di pesan baru
    st.rerun()

# Footer
st.divider()
st.caption("Hanya teman curhat AI • Bukan pengganti psikolog profesional • Gunakan dengan bijak")