import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP & STYLING ---
st.set_page_config(page_title="Tanz-Atelier: KI-Analyse", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FÜR DAS TOCA-BOCA-INSPIRIERTE DESIGN ---
st.markdown("""
<style>
    /* Hintergrund: Dunkelgrüner Samt-Verlauf */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #023020 0%, #011F13 100%);
        color: #FDFDD0; /* Warmes Weiß für guten Kontrast */
    }
    
    /* Goldene Überschriften ohne Glitzer */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* TOCA BOCA GLÜHBIRNEN AN SEILEN (In den oberen Ecken) */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            /* Linkes Seil mit Glühbirne */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 40px, transparent 40px),
            radial-gradient(circle at 10% 50px, #ffffff 0%, #fffae6 8px, rgba(255, 215, 0, 0.6) 20%, transparent 55%),
            
            /* Rechtes Seil mit Glühbirne */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 40px, transparent 40px),
            radial-gradient(circle at 90% 50px, #ffffff 0%, #fffae6 8px, rgba(255, 215, 0, 0.6) 20%, transparent 55%),
            
            /* Sanftes Hintergrundleuchten im Zentrum von den Lampen oben */
            radial-gradient(circle at 50% 0%, rgba(255, 215, 0, 0.08) 0%, transparent 40%);
        
        /* Exakte Positionierung der Seile und Birnen links (10%) und rechts (90%) */
        background-position: 
            10% 0px, 10% 10px,
            90% 0px, 90% 10px,
            50% 0px;
        background-size: 
            3px 40px, 100px 100px,
            3px 40px, 100px 100px,
            100% 100%;
        background-repeat: no-repeat;
        pointer-events: none;
        z-index: 1;
    }
    
    /* Styling für die Upload-Boxen */
    [data-testid="stFileUploader"] {
        border: 2px dashed #FFD700;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.04);
    }
    
    /* Goldene Box für das Feedback der KI */
    .gold-box {
        background-color: rgba(255, 215, 0, 0.05);
        border: 1px solid #FFD700;
        padding: 23px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER BEREICH ---
st.markdown("<h1 style='text-align: center; margin-top: 30px;'>Willkommen im Tanz-Atelier</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FDFDD0;'>Lass deine Pose im warmen Glanz der KI analysieren. Wir feilen gemeinsam an deiner Technik.</p>", unsafe_allow_html
