import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Echte Ballett-Analyse KI", layout="wide")

st.title("🩰 Unerbittliche Ballett-Analyse-KI")
st.write("Lade deine Fotos hoch. Das neuronale Netz scannt deine Pose völlig selbstständig und deckt Fehler schonungslos auf.")

# --- API-KEY AUTOMATISCH LADEN ---
# Versucht zuerst, den Key aus den Streamlit Secrets zu laden, ansonsten aus der Sidebar
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    api_key = st.sidebar.text_input("Google API Key hier eintragen:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
else:
    genai.configure(api_key=api_key)

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
    if not api_key:
        st.error("🛑 Die Analyse kann nicht starten, weil der API-Key fehlt. Bitte trage ihn links in der Leiste ein oder hinterlege ihn in den Streamlit Secrets.")
    else:
        st.divider()
        with st.spinner("🧠 Das neuronale Netz scannt deine Fotos und vergleicht die Haltung..."):
            try:
                # Nutzen des multimodalen Modells für Bildanalyse
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Der unerbittliche Arbeitsauftrag an die KI
                prompt = (
                    "Du bist ein extrem strenger, unerbittlicher Ballettmeister einer Elite-Akademie. "
                    "Analysiere und vergleiche das zweite Bild (Deine Ausführung) haargenau mit dem ersten Bild (Profi). "
                    "Achte penibel auf typische Fehler wie einen Bananenfuß (unsaubere Fußstreckung), "
                    "fehlendes Spotting bei Drehungen (falsche Kopfhaltung/Blick), hochgezogene Schultern, "
                    "durchhängende Ellbogen oder eine instabile Körperachse. "
                    "Sei extrem kritisch! Wenn Fehler vorliegen, benenne sie direkt und knallhart. "
                    "Sag nur das, was auf dem zweiten Bild wirklich falsch ist. Wenn ein Bereich gut ist, kritisiere ihn nicht künstlich, "
                    "aber bleibe insgesamt auf Profi-Niveau unnachgiebig. "
                    "Gib am Ende eine ehrliche Bewertung in Prozent (0 bis 100%) ab. "
                    "Antworte strukturiert in klaren Stichpunkten auf Deutsch."
                )
                
                # Senden an die API
                response = model.generate_content([prompt, profi_img, user_img])
                
                st.success("✅ Bildanalyse abgeschlossen!")
                
                # Ausgabe des echten Ergebnisses
                st.header("📋 Das Urteil des digitalen Ballettmeisters")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Fehler bei der KI-Analyse: {e}")
