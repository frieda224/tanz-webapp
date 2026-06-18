import streamlit as st
from PIL import Image
import google.generativeai as genai
import numpy as np

# --- SEITEN-SETUP & STYLING ---
# Wir nutzen dunkles Grün als Basisthema
st.set_page_config(page_title="Tanz-Atelier: KI-Analyse", layout="wide", initial_sidebar_state="collapsed")

# --- INDIVIDUELLES CSS FÜR DAS DESIGN ---
st.markdown("""
<style>
    /* Hintergrund & Grundfarben */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #023020 0%, #011F13 100%);
        color: #FDFDD0; /* Warmes Off-White für Text */
    }
    
    /* Goldene Akzente */
    h1, h2, h3, .stMetric {
        color: #FFD700 !important; /* Gold */
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    /* "Glühbirnen"-Lichteffekt */
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
    
    /* Boxen & Upload-Bereiche */
    [data-testid="stFileUploader"] {
        border: 2px dashed #FFD700;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        background-color: rgba(255, 215, 0, 0.1);
        border-color: #FDFDD0;
    }
    
    /* Erfolg & Warnung anpassen */
    .stAlert {
        border-radius: 10px;
    }
    div[data-testid="stAlert"] {
        background-color: rgba(0, 50, 0, 0.6);
        border: 1px solid #FFD700;
        color: #FDFDD0;
    }
    
    /* Die rote Fehlermeldung von Streamlit lassen wir für 404, 
       aber für die API-Meldung machen wir sie weicher. */
    .css-kh5e70 { 
        background-color: rgba(139, 0, 0, 0.6) !important;
    }
    
    /* Goldenes Markdown-Urteil */
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

# --- KEY EINGABE ÜBER DIE WEBSEITE (SICHER) ---
st.sidebar.markdown("<h2 style='color: #FFD700;'>🔑 Dein privater Zugang</h2>", unsafe_type_html=True)
st.sidebar.write("Füge hier deinen Google API-Key ein, um die KI-Verbindung zu aktivieren.")
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
    profi_file = st.file_uploader("Lade das Foto eines Profis hoch", type
