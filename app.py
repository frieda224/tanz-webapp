import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP & STYLING ---
st.set_page_config(page_title="Tanz-Atelier: KI-Analyse", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FÜR DAS TOCA-BOCA-INSPIRIERTE DESIGN ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #023020 0%, #011F13 100%);
        color: #FDFDD0;
    }
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* 3 HÄNGENDE GLÜHBIRNEN PRO SEITE */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 1;
        background-repeat: no-repeat;
        background-image: 
            /* --- LINKE SEITE (3 Lampen) --- */
            /* Lampe 1: Lang (ganz links bei 5%) */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 80px, transparent 80px),
            radial-gradient(circle at 5% 90px, #ffffff 0%, #fffae6 6px, rgba(255, 215, 0, 0.5) 15%, transparent 40%),
            /* Lampe 2: Mittel (bei 10%) */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 50px, transparent 50px),
            radial-gradient(circle at 10% 60px, #ffffff 0%, #fffae6 6px, rgba(255, 215, 0, 0.5) 15%, transparent 40%),
            /* Lampe 3: Kurz (bei 15%) */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 30px, transparent 30px),
            radial-gradient(circle at 15% 40px, #ffffff 0%, #fffae6 6px, rgba(255, 215, 0, 0.5) 15%, transparent 40%),
            
            /* --- RECHTE SEITE (3 Lampen) --- */
            /* Lampe 4: Lang (ganz rechts bei 95%) */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 80px, transparent 80px),
            radial-gradient(circle at 95% 90px, #ffffff 0%, #fffae6 6px, rgba(255, 215, 0, 0.5) 15%, transparent 40%),
            /* Lampe 5: Mittel (bei 90%) */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 50px, transparent 50px),
            radial-gradient(circle at 90% 60px, #ffffff 0%, #fffae6 6px, rgba(255, 215, 0, 0.5) 15%, transparent 40%),
            /* Lampe 6: Kurz (bei 85%) */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 30px, transparent 30px),
            radial-gradient(circle at 85% 40px, #ffffff 0%, #fffae6 6px, rgba(255, 215, 0, 0.5) 15%, transparent 40%);
            
        background-position: 
            5% 0px, 5% 10px, 10% 0px, 10% 10px, 15% 0px, 15% 10px,
            95% 0px, 95% 10px, 90% 0px, 90% 10px, 85% 0px, 85% 10px;
        background-size: 
            2px 80px, 80px 80px, 2px 50px, 80px 80px, 2px 30px, 80px 80px,
            2px 80px, 80px 80px, 2px 50px, 80px 80px, 2px 30px, 80px 80px;
    }
    [data-testid="stFileUploader"] {
        border: 2px dashed #FFD700;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0
