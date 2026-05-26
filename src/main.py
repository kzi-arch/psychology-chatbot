import sys
from pathlib import Path

# Gunakan pysqlite3 untuk mengatasi masalah versi SQLite pada ChromaDB
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# Tambahkan direktori utama proyek ke sys.path agar Python mengenali modul 'src'
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from src.core.chatbot import PsychologyChatbot
from src.config.settings import settings
from src.utils.chat_storage import ChatStorage
from src.config.prompts import PERSONAS
from datetime import datetime

st.set_page_config(
    page_title="EmpathAI - Teman Curhat",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Dark Theme + Enhanced UI Styling
st.markdown("""
<style>
    /* Base Background */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    
    /* Sembunyikan Header/Footer Streamlit Bawaan */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}

    /* Styling Tombol Elegan */
    .stButton button { 
        border-radius: 20px; 
        border: 1px solid #333;
        background-color: #1E2127;
        color: #FAFAFA;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        box-shadow: 0 4px 10px rgba(255, 75, 75, 0.15);
    }

    /* Memperhalus Sidebar */
    [data-testid="stSidebar"] {
        background-color: #13151A;
        border-right: 1px solid #2E3036;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi
if "chatbot" not in st.session_state:
    st.session_state.chatbot = PsychologyChatbot(persona_key="empat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_storage" not in st.session_state:
    st.session_state.chat_storage = ChatStorage()

# ====================== SIDEBAR ======================
with st.sidebar:
    st.title("🧠 EmpathAI")
    st.caption("Teman Curhat Psikologi")

    st.divider()

    # Persona Selector
    st.write("**Pilih Persona**")
    persona_options = {f"{p['emoji']} {p['name']}" : key for key, p in PERSONAS.items()}
    selected_label = st.selectbox("Persona", options=list(persona_options.keys()), index=0)
    selected_key = persona_options[selected_label]

    if st.session_state.chatbot.current_persona != selected_key:
        st.session_state.chatbot.set_persona(selected_key)
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Simpan Chat", use_container_width=True):
            if st.session_state.messages:
                title = st.text_input("Judul:", f"Curhat {datetime.now().strftime('%d %B')}")
                if st.button("Simpan"):
                    st.session_state.chat_storage.save_chat(st.session_state.messages, title)
                    st.success("Tersimpan!")

    with col2:
        if st.button("📤 Export TXT", use_container_width=True):
            if st.session_state.messages:
                txt_content = "\n\n".join([f"{'👤 Kamu' if m['role']=='user' else '🧠 EmpathAI'}: {m['content']}" 
                                        for m in st.session_state.messages])
                st.download_button("Download", txt_content, f"empathai_{datetime.now().strftime('%Y%m%d')}.txt")

    st.divider()
    if st.button("🗑️ Hapus Riwayat", type="secondary"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_history()
        st.success("Riwayat dibersihkan.")

# ====================== MAIN CHAT ======================
st.markdown("<h1 style='text-align: center; color: #FF4B4B; padding-top: 1rem;'>💬 EmpathAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A0A0A0; font-size: 1.1em; margin-bottom: 2rem;'><strong>Aku di sini mendengarkanmu.</strong> Ceritakan apa yang kamu rasakan hari ini.</p>", unsafe_allow_html=True)

for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🧠"):
        st.markdown(msg["content"])
        
        if msg["role"] == "assistant":
            col1, col2 = st.columns([1,5])
            with col1:
                if st.button("👍", key=f"like{idx}"):
                    st.session_state.chat_storage.feedback_manager.save_feedback(
                        idx, st.session_state.messages[idx-1]["content"], msg["content"], 1
                    )
                    st.toast("Terima kasih atas feedbacknya ❤️")

# Input Chat
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("EmpathAI sedang mendengarkan..."):
            response = st.session_state.chatbot.get_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})