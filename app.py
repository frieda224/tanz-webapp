import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Tanz-Trainer", layout="wide")

st.title("🩰 Tanz-Trainer")
st.write("Vergleiche deine Pose mit einem Profi – Schnell, stabil und ohne Server-Abstürze!")

# --- SPALTEN FÜR DIE BILDER ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Profi-Referenz")
    profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Profi-Pose", use_container_width=True)

with col2:
    st.subheader("2. Deine Pose")
    user_file = st.file_uploader("Dein Foto hochladen", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Deine Pose", use_container_width=True)

# --- MANUELLE POSEN-ANALYSE (STABIL FÜR SCHULE & PRÄSENTATION) ---
if profi_file and user_file:
    st.divider()
    st.header("📋 Posen-Vergleich")
    st.write("Trage hier die geschätzten Gelenkwinkel ein, um die Haltung zu überprüfen:")

    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        winkel_profi = st.slider("Armwinkel beim Profi (in Grad)", 0, 180, 90)
        
    with col_w2:
        winkel_user = st.slider("Dein Armwinkel (in Grad)", 0, 180, 90)
        
    # Berechnung des Scores
    abweichung = abs(winkel_profi - winkel_user)
    score = max(0, 100 - abweichung)
    
    st.subheader(f"Ergebnis: {score}% Übereinstimmung")
    
    if score > 85:
        st.success("🌟 Sensationell! Deine Haltung stimmt fast perfekt mit dem Profi überein!")
    elif score > 60:
        st.warning("👍 Solide Leistung! Korrigiere deinen Armwinkel noch ein kleines bisschen.")
    else:
        st.error("❌ Große Abweichung. Schau dir den Armwinkel beim Profi noch einmal genau an!")
