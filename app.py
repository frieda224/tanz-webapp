import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Ballett-Meister KI (Gnadenlose Analyse)", layout="wide")

st.title("🩰 Ballett-Meister KI – Die ungeschminkte Wahrheit")
st.write("Im Ballett ist nichts jemals perfekt. Diese KI analysiert deine Haltung mit der Strenge einer professionellen Academie.")

# --- SPALTEN FÜR DIE BILDER ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Profi-Referenz (Idealbild)")
    profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Profi-Pose", use_container_width=True)

with col2:
    st.subheader("2. Deine Ausführung (Kritischer Blick)")
    user_file = st.file_uploader("Dein Foto hochladen", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Deine Pose zur Korrektur", use_container_width=True)

# --- UNERBITTLICHE BALLETT-ANALYSE ---
if profi_file and user_file:
    st.divider()
    st.header("🔍 Protokoll der Haltungsmängel")
    
    # Eingabe-Bereich
    col_inputs, col_errors = st.columns([2, 1])
    
    with col_inputs:
        st.markdown("### 📐 Gelenk- und Achsenabgleich")
        st.write("Stelle die Slider nach bestem Wissen ein. Die KI wird die Fehler aufdecken:")
        
        kopf_profi = st.slider("Kopf-Winkel Profi", 0, 180, 90, key="k_profi")
        kopf_user = st.slider("Dein Kopf-Winkel", 0, 180, 90, key="k_user")
        
        arm_profi = st.slider("Arm-Winkel Profi", 0, 180, 90, key="a_profi")
        arm_user = st.slider("Dein Arm-Winkel", 0, 180, 90, key="a_user")
        
        fuss_profi = st.slider("Fuß-Winkel Profi", 0, 180, 90, key="f_profi")
        fuss_user = st.slider("Dein Fuß-Winkel", 0, 180, 90, key="f_user")

    with col_errors:
        st.markdown("### 🚨 Sichtbare technische Patzer")
        st.write("Hake die Fehler an, die auf deinem Foto zu sehen sind:")
        
        fehler_drehung = st.checkbox("Aus der Drehung gefallen / Achse verloren", key="f_drehung")
        fehler_spotten = st.checkbox("Kopf spottet nicht (Blick verloren)", key="f_spotten")
        fehler_banane = st.checkbox("Bananenfuß (Unsaubere Fußstreckung)", key="f_banane")

    # --- BERECHNUNG MIT BALLETT-ABZUG ---
    score_kopf = max(0, 100 - abs(kopf_profi - kopf_user))
    score_arm = max(0, 100 - abs(arm_profi - arm_user))
    score_fuss = max(0, 100 - abs(fuss_profi - fuss_user))
    
    # Basis-Score aus den Reglern
    basis_score = (score_kopf + score
