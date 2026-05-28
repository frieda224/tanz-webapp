import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Ballett-Meister KI (Gnadenlose Analyse)", layout="wide")

st.title("🩰 Ballett-Meister KI – Die ungeschminkte Wahrheit")
st.write("Im Ballett ist nichts jemals perfekt. Diese KI analysiert deine Haltung mit der Strenge einer professionellen Academie.")

# --- BILDER HOCHLADEN ---
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
    
    col_inputs, col_errors = st.columns([2, 1])
    
    with col_inputs:
        st.markdown("### 📐 Gelenk- und Achsenabgleich")
        kopf_profi = st.slider("Kopf-Winkel Profi", 0, 180, 90, key="k_profi")
        kopf_user = st.slider("Dein Kopf-Winkel", 0, 180, 90, key="k_user")
        
        arm_profi = st.slider("Arm-Winkel Profi", 0, 180, 90, key="a_profi")
        arm_user = st.slider("Dein Arm-Winkel", 0, 180, 90, key="a_user")
        
        fuss_profi = st.slider("Fuß-Winkel Profi", 0, 180, 90, key="f_profi")
        fuss_user = st.slider("Dein Fuß-Winkel", 0, 180, 90, key="f_user")

    with col_errors:
        st.markdown("### 🚨 Sichtbare technische Patzer")
        fehler_drehung = st.checkbox("Aus der Drehung gefallen / Achse verloren", key="f_drehung")
        fehler_spotten = st.checkbox("Kopf spottet nicht (Blick verloren)", key="f_spotten")
        fehler_banane = st.checkbox("Bananenfuß (Unsaubere Fußstreckung)", key="f_banane")

    # --- HIER WAR DER FEHLER: JETZT ABSOLUT SICHER BERECHNET ---
    diff_k = abs(kopf_profi - kopf_user)
    diff_a = abs(arm_profi - arm_user)
    diff_f = abs(fuss_profi - fuss_user)
    
    reiner_schnitt = (diff_k + diff_a + diff_f) / 3
    basis_score = 100 - reiner_schnitt

    # Abzüge berechnen
    abzug = 0
    kritik_punkte = []
    
    if fehler_drehung:
        abzug += 30
        kritik_punkte.append("🛑 **Achsen-Kollaps:** Aus der Drehung gefallen. Ohne Core-Spannung bleibt die Pirouette instabil.")
    if fehler_spotten:
        abzug += 25
        kritik_punkte.append("🛑 **Kopf-Verzögerung:** Kein Spotting! Kopf muss peitschenknallartig drehen.")
    if fehler_banane:
        abzug += 25
        kritik_punkte.append("🛑 **Bananenfuß:** Unsaubere Fußstreckung! Gelenk knickt ein.")

    gesamtscore = basis_score - abzug
    
    if gesamtscore > 95:
        gesamtscore = 92.5
        
    gesamtscore = max(0, gesamtscore)

    # --- AUSGABE ---
    st.divider()
    st.header("📋 Das Urteil des Ballettmeisters")
    
    col_fb1, col_fb2 = st.columns(2)
    
    with col_fb1:
        st.subheader("📊 Unerbittliche Punktebewertung")
        if gesamtscore >= 85:
            st.warning(f"⚠️ {gesamtscore:.1f}% – Sauberer Ansatz, ABER weit entfernt von Perfektion. Es fehlt an Körperspannung.")
        elif gesamtscore >= 60:
            st.error(f"❌ {gesamtscore:.1f}% – Mangelhafte Ausführung! Grobe Defizite in der Platzierung.")
        else:
            st.error(f"💀 {gesamtscore:.1f}% – Inakzeptabel! Gehe zurück an die Stange (Barre).")
            
    with col_fb2:
        st.markdown("### 📝 Unverzügliche Korrektur-Aufgaben")
        if kritik_punkte:
            for kritik in kritik_punkte:
                st.write(kritik)
        
        st.markdown("---")
        st.markdown("##### 🩰 Mikro-Korrekturen (Die immer gelten):")
        st.write("• **Schultern:** Drücke die Schulterblätter aktiv nach unten!")
        st.write("• **Finger:** Die Hände wirken verkrampft. Finger weich verlängern.")
        st.write("• **Standbein:** Das Knie des Standbeins ist nicht maximal durchgestreckt!")

        st.text_area("Eigenanalyse für das Vortragsprotokoll:", placeholder="Welche Korrekturen wurden heute umgesetzt?")
