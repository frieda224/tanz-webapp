import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP & STYLING ---
st.set_page_config(page_title="Tanz-Atelier: KI-Analyse", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FÜR DAS DUNKELGRÜNE LICHTERMEER ---
st.markdown("""
<style>
    /* Hintergrund: Dunkelgrüner Samt-Verlauf */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle, #023020 0%, #011F13 100%);
        color: #FDFDD0; /* Warmes Weiß für guten Kontrast */
    }
    
    /* Goldene Überschriften mit leichtem Schein */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
    }
    
    /* "Glühbirnen"-Effekt: Künstliche Lichtkegel von oben */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(circle at 15% 5%, rgba(255, 248, 220, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 85% 8%, rgba(255, 248, 220, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 50% 2%, rgba(255, 215, 0, 0.1) 0%, transparent 30%);
        pointer-events: none;
        z-index: 0;
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
st.markdown("<h1 style='text-align: center;'>✨ Willkommen im Tanz-Atelier ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FDFDD0;'>Lass deine Pose im warmen Glanz der KI analysieren. Wir feilen gemeinsam an deiner Technik.</p>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px; border-top: 1px solid rgba(255, 215, 0, 0.2);'></div>", unsafe_allow_html=True)

# --- SICHERE SCHLÜSSEL-EINGABE ---
st.sidebar.markdown("<h2 style='color: #FFD700;'>🔑 Dein Zugang</h2>", unsafe_allow_html=True)
api_key_input = st.sidebar.text_input("Gib hier deinen Google API-Key ein:", type="password")

if api_key_input:
    genai.configure(api_key=api_key_input)
    KI_BEREIT = True
    st.sidebar.success("✅ Verbindung zum Atelier steht!")
else:
    KI_BEREIT = False
    st.sidebar.warning("⚠️ Bitte gib links deinen API-Key ein, um zu starten.")

# --- BILDER HOCHLADEN ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center;'>1. Die ideale Form (Referenz)</h3>", unsafe_allow_html=True)
    profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Soll-Zustand (Profi)", use_container_width=True)

with col2:
    st.markdown("<h3 style='text-align: center;'>2. Deine Ausführung (Foto)</h3>", unsafe_allow_html=True)
    user_file = st.file_uploader("Dein Foto hochladen", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Deine Pose zur echten KI-Analyse", use_container_width=True)

# --- DER AUTOMATISCHE SCAN (NETTER & GERETTETE STRING-SYNTAX) ---
if profi_file and user_file:
    if not KI_BEREIT:
        st.error("🛑 Die automatische Analyse kann erst starten, wenn du deinen API-Key links eingetragen hast.")
    else:
        st.markdown("<div style='margin-top: 40px; border-top: 1px solid rgba(255, 215, 0, 0.2);'></div>", unsafe_allow_html=True)
        with st.spinner("💡 Wir dimmen das Licht... Der freundliche digitale Tanzmeister prüft deine Pose ganz genau..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Kompakt in einer Zeile, damit GitHub beim Speichern nichts zerbricht:
                prompt = "Du bist ein sehr erfahrener, aber zugewandter und freundlicher Ballettmeister. Analysiere und vergleiche das zweite Bild (Deine Ausführung) haargenau mit dem ersten Bild (Profi). Habe Respekt vor der gezeigten Leistung, sei aber präzise und konstruktiv. Erkenne die Position (z.B. Plié, Arabesque, Pirouette) und analysiere die Haltung passend dazu (z.B. Knieöffnung, Oberkörper oder Bananenfuß). Nenne NUR Fehler, die real auf dem Bild zu sehen sind. Deine Tipps sollen helfen, sich zu verbessern, und motivieren. Gib am Ende eine ehrliche, aber liebevolle Bewertung in Prozent (0-100%) ab. Antworte übersichtlich in Stichpunkten auf Deutsch."
                
                response = model.generate_content([prompt, profi_img, user_img])
                
                st.success("✅ Analyse erfolgreich abgeschlossen!")
                st.markdown("<h2 style='text-align: center;'>📋 Das Urteil des digitalen Tanzmeisters</h2>", unsafe_allow_html=True)
                st.markdown(f"<div class='gold-box'>{response.text}</div>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #FFD700; font-weight: bold; margin-top: 15px;'>✨ Bleib dran! Jedes Training bringt dich weiter.</p>", unsafe_allow_html=True)
                
            except Exception as e:
                try:
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model.generate_content([prompt, profi_img, user_img])
                    st.success("✅ Analyse erfolgreich abgeschlossen!")
                    st.markdown("<h2 style='text-align: center;'>📋 Das Urteil des digitalen Tanzmeisters</h2>", unsafe_allow_html=True)
                    st.markdown(f"<div class='gold-box'>{response.text}</div>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: #FFD700; font-weight: bold; margin-top: 15px;'>✨ Bleib dran! Jedes Training bringt dich weiter.</p>", unsafe_allow_html=True)
                except Exception as inner_e:
                    st.error(f"Fehler im Lichtermeer: {inner_e}")
