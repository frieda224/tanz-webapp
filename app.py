import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Echte Ballett-Analyse KI", layout="wide")

st.title("💡 Unerbittliche Ballett-Analyse-KI")
st.write("Lade deine Fotos hoch. Ein echtes neuronale Netz (Google Gemini) scannt deine Pose völlig selbstständig.")

# --- KI SCHLÜSSEL EINRICHTEN ---
# Du kannst dir unter aistudio.google.com kostenlos einen API-Key holen.
# Trage ihn hier ein oder nutze die Streamlit Secrets.
API_KEY = st.sidebar.text_input("Dein Google API Key:", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.sidebar.warning("⚠️ Bitte gib links deinen kostenlosen Google API-Key ein, damit die KI die Bilder scannen kann!")

# --- BILDER HOCHLADEN ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Profi-Referenz (Soll-Form)")
    profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Soll-Zustand (Profi)", use_container_width=True)

with col2:
    st.subheader("2. Deine Ausführung (Ist-Form)")
    user_file = st.file_uploader("Dein Foto hochladen", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Deine Pose zur automatischen Analyse", use_container_width=True)

# --- DER ECHTE AUTOMATISCHE SCAN ---
if profi_file and user_file:
    if not API_KEY:
        st.error("🛑 Die Analyse kann nicht starten, weil der API-Key in der linken Leiste fehlt.")
    else:
        st.divider()
        with st.spinner("🧠 Das neuronale Netz scannt deine Fotos und vergleicht die Haltung..."):
            try:
                # Wir nutzen das multimodale Modell "gemini-1.5-flash", das Bilder analysieren kann
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Der unerbittliche Arbeitsauftrag an die KI
                prompt = (
                    "Du bist ein extrem strenger, unerbittlicher Ballettmeister einer Elite-Akademie. "
                    "Analysiere und vergleiche das zweite Bild (Deine Ausführung) haargenau mit dem ersten Bild (Profi). "
                    "Achte penibel auf typische Fehler wie einen Bananenfuß (unsaubere Fußstreckung), "
                    "fehlendes Spotting bei Drehungen (falsche Kopfhaltung/Blick), hochgezogene Schultern, "
                    "durchhängende Ellbogen oder eine instabile Körperachse. "
                    "Sei extrem kritisch! Wenn Fehler vorliegen, benenne sie direkt und knallhart. "
                    "Gib am Ende eine ehrliche Bewertung in Prozent (0 bis 100%) ab, wobei 100% im Ballett unerreichbar ist. "
                    "Antworte strukturiert auf Deutsch."
                )
                
                # Wir schicken den Auftrag und BEIDE Bilder an Google
                response = model.generate_content([prompt, profi_img, user_img])
                
                st.success("✅ Bildanalyse erfolgreich durchgeführt!")
                
                # Ausgabe der echten KI-Antwort
                st.header("📋 Das Urteil des digitalen Ballettmeisters")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Fehler bei der KI-Analyse: {e}")
                st.info("Hinweis: Überprüfe, ob dein API-Key gültig ist.")
