import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Unerbittliche Ballett-Analyse KI", layout="wide")

st.title("🩰 Unerbittliche Ballett-Analyse-KI")
st.write("Lade deine Fotos hoch. Die KI scannt deine Pose völlig selbstständig und deckt Fehler unbarmherzig auf.")

# --- API-KEY AUS DEN SYSTEMEINSTELLUNGEN LADEN ---
# Holt sich den Schlüssel vollautomatisch aus den Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)
    KI_BEREIT = True
else:
    KI_BEREIT = False
    st.sidebar.warning("⚠️ Der GEMINI_API_KEY fehlt noch in den Streamlit Secrets!")
    # Ausweichoption, falls du ihn doch mal schnell eintippen willst:
    temp_key = st.sidebar.text_input("Oder hier temporär eingeben:", type="password")
    if temp_key:
        genai.configure(api_key=temp_key)
        KI_BEREIT = True

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
        st.error("🛑 Die automatische Analyse kann nicht starten, weil der Google API-Key nicht hinterlegt ist.")
    else:
        st.divider()
        with st.spinner("🧠 Das neuronale Netz analysiert deine Haltung im Vergleich zum Profi..."):
            try:
                # Das stabile, visuelle Modell von Google aufrufen
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Der glasklare Arbeitsauftrag an die KI: Keine Ausreden, nur echte Fehler!
                prompt = (
                    "Du bist ein extrem strenger, unnachgiebiger Ballettmeister einer Elite-Akademie. "
                    "Analysiere und vergleiche das zweite Bild (Deine Ausführung) haargenau mit dem ersten Bild (Profi). "
                    "Schaue genau, welche Position getanzt wird (z.B. ein Plié, eine Arabesque oder eine Pirouette). "
                    "Analysiere die Haltung passend zu dieser Position! Wenn es ein Plie ist, rede nicht über Spotting, "
                    "sondern über die Knieöffnung und den Oberkörper. Wenn es eine Streckung ist, achte extrem auf einen Bananenfuß. "
                    "Nenne NUR Fehler, die auf dem zweiten Bild wirklich und real zu sehen sind. Erfinde nichts! "
                    "Sei extrem kritisch auf Profi-Niveau. Gib am Ende eine ehrliche Bewertung in Prozent (0 bis 100%) ab. "
                    "Antworte übersichtlich in Stichpunkten auf Deutsch."
                )
                
                # Bilder an das Google-Rechenzentrum übergeben
                response = model.generate_content([prompt, profi_img, user_img])
                
                st.success("✅ Analyse erfolgreich abgeschlossen!")
                
                # Das unbestechliche Urteil ausgeben
                st.header("📋 Das Urteil des digitalen Ballettmeisters")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Fehler bei der Übertragung an die KI: {e}")
