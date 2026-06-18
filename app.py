import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Unerbittliche Ballett-Analyse KI", layout="wide")

st.title("🩰 Unerbittliche Ballett-Analyse-KI")
st.write("Lade deine Fotos hoch. Die KI scannt deine Pose völlig selbstständig.")

# --- SICHERE SCHLÜSSEL-EINGABE ÜBER DIE WEBSEITE ---
st.sidebar.header("🔑 KI-Verbindung")
api_key_input = st.sidebar.text_input("Gib hier deinen Google API-Key ein:", type="password")

if api_key_input:
    genai.configure(api_key=api_key_input)
    KI_BEREIT = True
    st.sidebar.success("✅ KI erfolgreich verbunden!")
else:
    KI_BEREIT = False
    st.sidebar.warning("⚠️ Bitte gib links deinen API-Key ein, um die Analyse zu starten.")

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
        st.image(user_img, caption="Deine Pose zur echten KI-Analyse", use_container_width=True)

# --- DER REALE AUTOMATISCHE SCAN ---
if profi_file and user_file:
    if not KI_BEREIT:
        st.error("🛑 Die automatische Analyse kann erst starten, wenn du deinen API-Key links in die Seitenleiste eingetragen hast.")
    else:
        st.divider()
        with st.spinner("🧠 Das neuronale Netz analysiert deine Haltung im Vergleich zum Profi..."):
            try:
                # GEÄNDERT: Wir nutzen 'gemini-2.5-flash', da dieses Modell das aktuellste ist 
                # und die alten v1beta-Fehler auf Servern umgeht.
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = (
                    "Du bist ein extrem strenger, unnachgiebiger Ballettmeister einer Elite-Akademie. "
                    "Analysiere und vergleiche das zweite Bild (Deine Ausführung) haargenau mit dem ersten Bild (Profi). "
                    "Schaue genau, welche Position getanzt wird (z.B. ein Plié, eine Arabesque oder eine Pirouette). "
                    "Analysiere die Haltung passend to dieser Position! Wenn es ein Plié ist, rede nicht über Spotting, "
                    "sondern über die Knieöffnung und den Oberkörper. Wenn es eine Streckung ist, achte extrem auf einen Bananenfuß. "
                    "Nenne NUR Fehler, die auf dem zweiten Bild wirklich und real zu sehen sind. Erfinde nichts! "
                    "Sei extrem kritisch auf Profi-Niveau. Gib am Ende eine ehrliche Bewertung in Prozent (0 bis 100%) ab. "
                    "Antworte übersichtlich in Stichpunkten auf Deutsch."
                )
                
                response = model.generate_content([prompt, profi_img, user_img])
                
                st.success("✅ Analyse erfolgreich abgeschlossen!")
                st.header("📋 Das Urteil des digitalen Ballettmeisters")
                st.markdown(response.text)
                
            except Exception as e:
                # Falls auch das fehlschlägt, versuchen wir als automatischen Fallback das absolut universelle Modell
                try:
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model.generate_content([prompt, profi_img, user_img])
                    st.success("✅ Analyse erfolgreich abgeschlossen!")
                    st.header("📋 Das Urteil des digitalen Ballettmeisters")
                    st.markdown(response.text)
                except Exception as inner_e:
                    st.error(f"Fehler bei der Übertragung an die KI: {inner_e}")
