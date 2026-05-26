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
    header {background-color: transparent !important;}

    /* Styling Tombol Elegan */
    .stButton > button { 
        border-radius: 12px !important; 
        border: 1px solid #3E4148 !important;
        background-color: #1B1E23 !important;
        color: #FAFAFA !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover {
        border-color: #FF4B4B !important;
        color: #FF4B4B !important;
        background-color: rgba(255, 75, 75, 0.05) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.15) !important;
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* Memperhalus Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111317 !important;
        border-right: 1px solid #2B2D31 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #2B2D31;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Style khusus Selectbox di Sidebar */
    div[data-baseweb="select"] > div {
        background-color: #1B1E23 !important;
        border-color: #3E4148 !important;
        border-radius: 8px !important;
    }

    /* --- UI Chat Bubbles Modern --- */
    [data-testid="stChatMessage"] {
        background-color: #1E2127;
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid #2B2D31;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }

    /* --- RESPONSIVE DESIGN (Mobile) --- */
    @media screen and (max-width: 768px) {
        h1 { font-size: 1.6rem !important; margin-top: -1rem !important; }
        p { font-size: 0.95rem !important; }
        
        /* Perkecil padding bubble chat di HP */
        [data-testid="stChatMessage"] {
            padding: 0.8rem;
            border-radius: 12px;
            margin-bottom: 0.8rem;
        }
        
        /* Atur jarak container utama agar tidak terlalu memakan layar */
        .block-container {
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Pastikan target sentuh (tap) optimal di mobile */
        .stButton > button { min-height: 44px; }
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
    st.markdown("""
    <div style='text-align: center; margin-bottom: 10px;'>
        <h2 style='margin-bottom: 0; color: #FF4B4B; font-weight: 700; letter-spacing: 1px;'>🧠 EmpathAI</h2>
        <p style='color: #8B949E; font-size: 0.9em; margin-top: 5px;'>Teman Curhat Psikologi</p>
    </div>
    """, unsafe_allow_html=True)

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
        with st.popover("💾 Simpan", use_container_width=True):
            if not st.session_state.messages:
                st.info("Belum ada chat.")
            else:
                title = st.text_input("Judul Chat:", f"Curhat {datetime.now().strftime('%d %B')}")
                if st.button("Simpan ke History", type="primary", use_container_width=True):
                    st.session_state.chat_storage.save_chat(st.session_state.messages, title)
                    st.success("Tersimpan!")

    with col2:
        if st.session_state.messages:
            txt_content = "\n\n".join([f"{'👤 Kamu' if m['role']=='user' else '🧠 EmpathAI'}: {m['content']}" 
                                    for m in st.session_state.messages])
            st.download_button("📤 Export", txt_content, f"empathai_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)
        else:
            st.button("📤 Export", disabled=True, use_container_width=True)

    st.divider()
    with st.popover("🗑️ Hapus Riwayat", use_container_width=True):
        st.write("Yakin ingin menghapus semua percakapan ini?")
        if st.button("Ya, Hapus!", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chatbot.clear_history()
            st.rerun()

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