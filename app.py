import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP & STYLING ---
st.set_page_config(page_title="Tanz-Atelier: KI-Analyse", layout="wide", initial_sidebar_state="collapsed")

# --- INDIVIDUELLES CSS FÜR DAS DESIGN ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #023020 0%, #011F13 100%);
        color: #FDFDD0;
    }
    h1, h2, h3, .stMetric {
        color: #FFD700 !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(255, 248, 220, 0.2) 0%, transparent 20%),
            radial-gradient(circle at 90% 15%, rgba(255, 248, 220, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 50% 5%, rgba(255, 215, 0, 0.1) 0%, transparent 30%);
        pointer-events: none;
        z-index: 0;
    }
    [data-testid="stFileUploader"] {
        border: 2px dashed #FFD700;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    [data-testid="stFileUploader"]:hover {
        background-color: rgba(255, 215, 0, 0.1);
        border-color: #FDFDD0;
    }
    div[data-testid="stAlert"] {
        background-color: rgba(0, 50, 0, 0.6);
        border: 1px solid #FFD700;
        color: #FDFDD0;
    }
    .gold-box {
        background-color: rgba(255, 215, 0, 0.05);
        border: 1px solid #FFD700;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_type_html=True)

# --- HEADER BEREICH ---
st.markdown("<h1 style='text-align: center;'>✨ Willkommen im Tanz-Atelier ✨</h1>", unsafe_type_html=True)
st.markdown("<p style='text-align: center; color: #FDFDD0;'>Lass deine Pose im warmen Glanz der KI analysieren. Wir feilen gemeinsam an deiner Technik.</p>", unsafe_type_html=True)
st.markdown("<div style='margin-bottom: 30px; border-top: 1px solid rgba(255, 215, 0, 0.2);'></div>", unsafe_type_html=True)

# --- KEY EINGABE ÜBER DIE WEBSEITE ---
st.sidebar.markdown("<h2 style='color: #FFD700;'>🔑 Dein privater Zugang</h2>", unsafe_type_html=True)
api_key_input = st.sidebar.text_input("API-Key:", type="password")

if api_key_input:
    genai.configure(api_key=api_key_input)
    KI_BEREIT = True
    st.sidebar.success("✅ Wir sind verbunden. Viel Erfolg!")
else:
    KI_BEREIT = False
    st.sidebar.warning("⚠️ Bitte gib zuerst deinen API-Key ein.")

# --- BILDER HOCHLADEN ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center;'>1. Die ideale Form (Referenz)</h3>", unsafe_type_html=True)
    profi_file = st.file_uploader("Lade das Foto eines Profis hoch", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Unser Vorbild (Soll-Form)", use_container_width=True)

with col2:
    st.markdown("<h3 style='text-align: center;'>2. Deine Ausführung (Foto)</h3>", unsafe_type_html=True)
    user_file = st.file_uploader("Lade dein eigenes Foto hoch", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Dein Scan (Ist-Form)", use_container_width=True)

# --- AUTOMATISCHE KI-ANALYSE ---
if profi_file and user_file:
    if not KI_BEREIT:
        st.warning("🛑 Fast geschafft! Um den Scan zu starten, gib bitte links deinen API-Key ein.")
    else:
        st.markdown("<div style='margin-top: 40px; border-top: 1px solid rgba(255, 215, 0, 0.2);'></div>", unsafe_type_html=True)
        with st.spinner("💡 Wir dimmen das Licht... Der digitale Ballettmeister prüft deine Pose ganz genau..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = (
                    "Du bist ein sehr erfahrener, aber zugewandter und freundlicher Ballettmeister einer Akademie. "
                    "Analysiere und vergleiche das zweite Bild (Deine Ausführung) haargenau
