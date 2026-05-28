import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Tanz-Trainer Pro", layout="wide")

st.title("🩰 Tanz-Trainer Pro")
st.write("Vergleiche Kopf, Arme und Füße mit dem Profi – Schnell, stabil und präzise!")

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

# --- ERWEITERTE POSEN-ANALYSE ---
if profi_file and user_file:
    st.divider()
    st.header("📋 Erweiterter Haltungs-Vergleich")
    st.write("Trage hier die geschätzten Winkel oder Werte für die verschiedenen Körperbereiche ein:")

    # Drei Spalten für die drei Bereiche (Kopf, Arme, Füße)
    col_k, col_a, col_f = st.columns(3)
    
    with col_k:
        st.markdown("### 👤 Kopfhaltung")
        kopf_profi = st.slider("Kopf-Winkel Profi", 0, 180, 90, key="k_profi")
        kopf_user = st.slider("Dein Kopf-Winkel", 0, 180, 90, key="k_user")
        abweichung_kopf = abs(kopf_profi - kopf_user)
        score_kopf = max(0, 100 - abweichung_kopf)
        st.metric("Übereinstimmung Kopf", f"{score_kopf:.0f}%")

    with col_a:
        st.markdown("### 💪 Armhaltung")
        arm_profi = st.slider("Arm-Winkel Profi", 0, 180, 90, key="a_profi")
        arm_user = st.slider("Dein Arm-Winkel", 0, 180, 90, key="a_user")
        abweichung_arm = abs(arm_profi - arm_user)
        score_arm = max(0, 100 - abweichung_arm)
        st.metric("Übereinstimmung Arme", f"{score_arm:.0f}%")
        
    with col_f:
        st.markdown("### 🦵 Fuß- & Beinstellung")
        fuss_profi = st.slider("Fuß-Winkel Profi", 0, 180, 90, key="f_profi")
        fuss_user = st.slider("Dein Fuß-Winkel", 0, 180, 90, key="f_user")
        abweichung_fuss = abs(fuss_profi - fuss_user)
        score_fuss = max(0, 100 - abweichung_fuss)
        st.metric("Übereinstimmung Füße", f"{score_fuss:.0f}%")
        
    # --- GESAMTERGEBNIS ---
    st.divider()
    gesamtscore = (score_kopf + score_arm + score_fuss) / 3
    st.subheader(f"📊 Gesamt-Ergebnis: {gesamtscore:.1f}% Übereinstimmung")
    
    # --- ZWEI SPALTEN FÜR FEEDBACK & KORREKTUR-NOTIZEN ---
    col_fb1, col_fb2 = st.columns(2)
    
    with col_fb1:
        st.markdown("### 🤖 KI-Feedback")
        if gesamtscore > 85:
            st.success("🌟 Sensationell! Deine Gesamthaltung stimmt fast perfekt mit dem Profi überein!")
        elif gesamtscore > 60:
            st.warning("👍 Gute Ansätze! Schau dir oben die einzelnen Werte an, wo es noch Abweichungen gibt.")
        else:
            st.error("❌ Größere Abweichungen in der Pose. Nutze die Slider, um Schritt für Schritt zu korrigieren.")
            
    with col_fb2:
        st.markdown("### 📝 Deine Korrektur-Notizen")
        korrektur_text = st.text_area(
            "Welche Details möchtest du korrigieren?",
            placeholder="Z.B.: Kopf gerader halten, linken Fuß weiter nach außen drehen...",
            key="korrektur"
        )
        
        if korrektur_text:
            st.info(f"**Gespeicherte Korrektur-Aufgaben:**\n{korrektur_text}")
