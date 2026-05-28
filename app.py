import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Tanz-Trainer Pro (Kritische Analyse)", layout="wide")

st.title("🩰 Tanz-Trainer Pro – Fehleranalyse")
st.write("Echte Fehlererkennung. Diese KI korrigiert dich knallhart, damit du wirklich lernen kannst!")

# --- SPALTEN FÜR DIE BILDER ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Profi-Referenz (Soll-Zustand)")
    profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Perfekte Profi-Pose", use_container_width=True)

with col2:
    st.subheader("2. Deine Pose (Ist-Zustand)")
    user_file = st.file_uploader("Dein Foto hochladen", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Deine Pose zur Analyse", use_container_width=True)

# --- ERWEITERTE, KRITISCHE POSEN-ANALYSE ---
if profi_file and user_file:
    st.divider()
    st.header("🔍 Detaillierte Haltungs- und Fehleranalyse")
    
    # Linke Spalte: Die Schieberegler für die Winkel
    col_inputs, col_errors = st.columns([2, 1])
    
    with col_inputs:
        st.markdown("### 📐 Winkel-Abgleich")
        st.write("Vergleiche die Positionen grob über die Regler:")
        
        kopf_profi = st.slider("Kopf-Winkel Profi", 0, 180, 90, key="k_profi")
        kopf_user = st.slider("Dein Kopf-Winkel", 0, 180, 90, key="k_user")
        
        arm_profi = st.slider("Arm-Winkel Profi", 0, 180, 90, key="a_profi")
        arm_user = st.slider("Dein Arm-Winkel", 0, 180, 90, key="a_user")
        
        fuss_profi = st.slider("Fuß-Winkel Profi", 0, 180, 90, key="f_profi")
        fuss_user = st.slider("Dein Fuß-Winkel", 0, 180, 90, key="f_user")

    # Reichte Spalte: DIE FEHLER-CHECKBOXEN (NEU!)
    with col_errors:
        st.markdown("### 🚨 Technische Fehler")
        st.write("Welche Fehler sind auf deinem Foto real zu sehen?")
        
        fehler_drehung = st.checkbox("Aus der Drehung gefallen / Instabil", key="f_drehung")
        fehler_spotten = st.checkbox("Kopf spottet nicht (Blick fixiert nicht)", key="f_spotten")
        fehler_banane = st.checkbox("Bananenfuß (Fuß unsauber gestreckt)", key="f_banane")

    # --- MATHEMATISCHE BERECHNUNG ---
    score_kopf = max(0, 100 - abs(kopf_profi - kopf_user))
    score_arm = max(0, 100 - abs(arm_profi - arm_user))
    score_fuss = max(0, 100 - abs(fuss_profi - fuss_user))
    
    # Basis-Score aus den Winkeln
    gesamtscore = (score_kopf + score_arm + score_fuss) / 3
    
    # --- MALUS-SYSTEM: PUNKTABZUG FÜR FEHLER ---
    st.divider()
    st.header("📋 KI-Auswertung und Korrekturanweisung")
    
    kritik_punkte = []
    
    if fehler_drehung:
        gesamtscore -= 25
        kritik_punkte.append("❌ **Stabilitäts-Fehler:** Du bist aus der Drehung gefallen. Achte auf deine Körperspannung im Core (Bauch/Rücken) und halte die Achse stabil.")
    
    if fehler_spotten:
        gesamtscore -= 20
        kritik_punkte.append("❌ **Spotting-Fehler:** Der Kopf spottet nicht! Du musst den Blick so lange wie möglich auf einen festen Punkt vor dir richten und den Kopf am Ende der Drehung am schnellsten herumholen. Sonst verlierst du die Orientierung.")
        
    if fehler_banane:
        gesamtscore -= 20
        kritik_punkte.append("❌ **Bananenfuß-Fehler:** Unsaubere Fußstreckung (Bananenfuß)! Der Fuß knickt in der Spitze ein. Strecke die Fußgelenke aktiv durch und ziehe die Zeilen in eine saubere Linie verlängernd zum Bein.")

    # Score darf nicht unter 0 sinken
    gesamtscore =
