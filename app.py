import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP & STYLING ---
st.set_page_config(page_title="Tanz-Atelier: KI-Analyse", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (TOCA BOCA DESIGN) ---
st.markdown("""
<style>
    /* Hintergrund: Dunkelgrüner Samt-Verlauf */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #023020 0%, #011F13 100%);
        color: #FDFDD0;
    }
    
    /* Goldene Überschriften */
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
            linear-gradient(to bottom, #4a3525 0px, #4a3525 120px, transparent 120px),
            radial-gradient(circle at 5% 135px, #ffffff 0%, #fffae6 10px, rgba(255, 215, 0, 0.6) 25%, transparent 55%),
            linear-gradient(to bottom, #4a3525 0px, #4a3525 80px, transparent 80px),
            radial-gradient(circle at 9% 95px, #ffffff 0%, #fffae6 10px, rgba(255, 215, 0, 0.6) 25%, transparent 55%),
            linear-gradient(to bottom, #4a3525 0px, #4a3525 40px, transparent 40px),
            radial-gradient(circle at 13% 55px, #ffffff 0%, #fffae6 10px, rgba(255, 215, 0, 0.6) 25%, transparent 55%),
            
            /* --- RECHTE SEITE (3 Lampen) --- */
            linear-gradient(to bottom, #4a3525 0px, #4a3525 120px, transparent 120px),
            radial-gradient(circle at 95% 135px, #ffffff 0%, #fffae6 10px, rgba(255, 215, 0, 0.6) 25%, transparent 55%),
            linear-gradient(to bottom, #4a3525 0px, #4a3525 80px, transparent 80px),
            radial-gradient(circle at 91% 95px, #ffffff 0%, #fffae6 10px, rgba(255, 215, 0, 0.6) 25%, transparent 55%),
            linear-gradient(to bottom, #4a3525 0px, #4a3525 40px, transparent 40px),
            radial-gradient(circle at 87% 55px, #ffffff 0%, #fffae6 10px, rgba(255, 215, 0, 0.6) 25%, transparent 55%);
            
        background-position: 
            5% 0px, 5% 0px, 9% 0px, 9% 0px, 13% 0px, 13% 0px,
            95% 0px, 95% 0px, 91% 0px,
