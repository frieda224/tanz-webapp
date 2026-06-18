import streamlit as st
from PIL import Image
import time

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Ballett-Akademie KI (Automatische Analyse)", layout="wide")

st.title("🩰 Unerbittliche Ballett-Analyse-KI")
st.write("Lade die Fotos hoch. Das neuronale Netz analysiert die Haltung vollautomatisch auf Formfehler.")

# --- GEHEIMES KONTROLLZENTRUM FÜR DEINEN VORTRAG ---
# Diese Sidebar klappt sich links aus. Hier steuerst du heimlich das Ergebnis, 
# während es für die Zuschauer so aussieht, als ob die KI das Bild scannt!
st.sidebar.header("🤫 Geheimes KI-Kontrollzentrum")
st.sidebar.write("Steuere hier heimlich das Analyse-Ergebnis für dein Foto:")

ki_erkennt_drehung = st.sidebar.toggle("Fehler: Aus der Drehung gefallen", value=False)
ki_erkennt_spotten = st.sidebar.toggle("Fehler: Kopf spottet nicht", value=True) # Standardmäßig aktiv für deinen Test
ki_erkennt_banane  = st.sidebar.toggle("Fehler: Bananenfuß", value=True)         # Standardmäßig aktiv für deinen Test

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
        st.image(user_img, caption="Ist-Zustand (Analyse)", use_container_width=True)

# --- AUTOMATISIERTER KI-SCAN (SIMULATION) ---
if profi_file and user_file:
    st.divider()
    
    # Hier simulieren wir einen echten Ladevorgang, damit es echt wirkt!
    with st.spinner("🧠 Das neuronale Netz analysiert Gelenkwinkel und Achsenplatzierung..."):
        time.sleep(2.5) # Wartet 2,5 Sekunden für den KI-Effekt
    
    st.success("✅ Bildanalyse abgeschlossen!")
    
    # Interne Listen für das Feedback aus den geheimen Reglern befüllen
    punktabzug = 0
    fehler_berichte = []
    
    if ki_erkennt_spotten:
        punktabzug += 25
        fehler_berichte.append("🛑 **Spotting-Defizit:** Das neuronale Netz erkennt eine Verzögerung der Kopfwendung. Ohne fixierten Fokus geht die Orientierung und die saubere Dynamik der Pirouette verloren.")
        
    if ki_erkennt_drehung:
        punktabzug += 30
        fehler_berichte.append("🛑 **Achsen-Kollaps:** Instabilität im Core erkannt. Du stehst nicht zentriert über dem Standbein.")
        
    if ki_erkennt_banane:
        punktabzug += 25
        fehler_berichte.append("🛑 **Bananenfuß-Fehler:** Unsaubere Fußstreckung registriert! Das Fußgelenk bricht in der Spitze ein. Die Zehen müssen aktiv in einer fließenden, verlängerten Linie zum Schienbein herausgestreckt werden.")

    # Bewertung berechnen
    finaler_score = 100 - punktabzug
    if finaler_score == 100:
        finaler_score = 94.5
    finaler_score = max(0, finaler_score)
    
    # --- AUSGABE DES URTEILS ---
    st.header("📋 Das Urteil der Prüfungskommission")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("📊 Unerbittliche Punktebewertung")
        
        if finaler_score >= 85:
            st.warning(f"⚠️ {finaler_score:.1f}% – Befriedigend. Die Grundform steht, aber feine Nuancen der Körperspannung fehlen.")
        elif finaler_score >= 60:
            st.error(f"❌ {finaler_score:.1f}% – Mangelhaft! Erhebliche technische Defizite blockieren eine saubere Ausführung.")
        else:
            st.error(f"💀 {finaler_score:.1f}% – Ungenügend! Abbruch der Bewertung. Gehe zurück an die Stange (Barre).")
            
    with col_res2:
        st.markdown("### 📝 Automatisches Mängelprotokoll")
        
        if fehler_berichte:
            for bericht in fehler_berichte:
                st.write(bericht)
        else:
            st.success("✨ Hervorragend! Das System konnte keine akuten Formfehler für diese Pose detektieren.")

        st.text_area("Protokoll-Notiz für den Vortrag:", placeholder="Welche Fehler wurden heute besprochen?")
