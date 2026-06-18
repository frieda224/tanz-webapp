 import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Ballett-Analyse Protokoll", layout="wide")

st.title("🩰 Akademisches Ballett-Analyse-Protokoll")
st.write("Echte Fehleranalyse. Es wird nur protokolliert, was real bemängelt wurde.")

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

# --- FEHLER-PROTOKOLLIERUNG ---
if profi_file and user_file:
    st.divider()
    st.header("🔍 Protokollierung spezifischer Haltungsmängel")
    st.write("Wähle aus, welche Fehler auf dem Foto real vorliegen:")
    
    # Listen für die Berechnung und das Feedback
    punktabzug = 0
    fehler_berichte = []
    
    # Spalten-Layout für die Checkboxen
    col_k1, col_k2 = st.columns(2)
    
    with col_k1:
        st.markdown("### 👤 Kopf & Oberkörper")
        spotten_fehler = st.checkbox("Kopf spottet nicht / Blick fixiert nicht", key="chk_spotten")
        if spotten_fehler:
            punktabzug += 25
            fehler_berichte.append("🛑 **Spotting-Defizit:** Der Kopf verzögert in der Drehung. Ohne fokussierten Blick geht die Orientierung und die saubere Dynamik der Pirouette verloren.")
            
        schulter_fehler = st.checkbox("Schultern hochgezogen (Verkrampfung)", key="chk_schulter")
        if schulter_fehler:
            punktabzug += 15
            fehler_berichte.append("🛑 **Schulter-Platzierung:** Die Schultern wandern zu den Ohren. Drücke die Schulterblätter aktiv nach unten, um die Halslinie zu wahren.")

        st.markdown("### 💪 Arme & Hände")
        ellbogen_fehler = st.checkbox("Ellbogen hängen durch / Keine runde Form (Port de bras)", key="chk_ellbogen")
        if ellbogen_fehler:
            punktabzug += 15
            fehler_berichte.append("🛑 **Arm-Geometrie:** Die Ellbogen fallen ab. Im Ballett halten die Arme eine stolze, getragene, runde Form.")
            
        finger_fehler = st.checkbox("Hände verkrampft / Starre Finger", key="chk_finger")
        if finger_fehler:
            punktabzug += 10
            fehler_berichte.append("🛑 **Ästhetik-Fehler:** Die Hände wirken starr. Die Finger müssen die Bewegung weich verlängern.")

    with col_k2:
        st.markdown("### 🦵 Beine & Stand")
        achse_fehler = st.checkbox("Aus der Drehung gefallen / Achse verloren", key="chk_achse")
        if achse_fehler:
            punktabzug += 30
            fehler_berichte.append("🛑 **Achsen-Kollaps:** Du stehst nicht zentriert über dem Standbein. Der Core (Bauch/Rücken) muss maximal stabilisiert werden.")
            
        knie_fehler = st.checkbox("Standbein-Knie nicht maximal durchgestreckt", key="chk_knie")
        if knie_fehler:
            punktabzug += 15
            fehler_berichte.append("🛑 **Instabilität im Knie:** Das Knie des Standbeins ist leicht gebeugt. Verliere niemals die vertikale Streckung im Raum!")

        st.markdown("### 🩰 Füße (Spezifische Abfrage)")
        bananen_fehler = st.checkbox("Bananenfuß (Unsaubere, eingeknickte Fußstreckung)", key="chk_banane")
        if bananen_fehler:
            punktabzug += 25
            fehler_berichte.append("🛑 **Bananenfuß:** Unsaubere Fußstreckung! Das Fußgelenk bricht in der Spitze ein. Du musst die Zehen aktiv in einer fließenden, verlängerten Linie zum Schienbein herausstrecken.")

    # --- BEWERTUNG BERECHNEN ---
    finaler_score = 100 - punktabzug
    
    # Kleine akademische Deckelung: Ballett ist nie absolut 100% perfekt.
    if finaler_score == 100:
        finaler_score = 95.0
    finaler_score = max(0, finaler_score)
    
    # --- AUSGABE DES URTEILS ---
    st.divider()
    st.header("📋 Das Urteil der Prüfungskommission")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("📊 Bewertungsergebnis")
        
        if finaler_score >= 85:
            st.warning(f"⚠️ {finaler_score:.1f}% – Befriedigend. Die Grundform steht.")
        elif finaler_score >= 60:
            st.error(f"❌ {finaler_score:.1f}% – Mangelhaft! Erhebliche technische Defizite blockieren eine saubere Ausführung.")
        else:
            st.error(f"💀 {finaler_score:.1f}% – Ungenügend! Abbruch der Bewertung. Gehe zurück an die Stange (Barre) und arbeite an den Basics.")
            
    with col_res2:
        st.markdown("### 📝 Reales Mängelprotokoll")
        
        # HIER DIE STRENGE LOGIK: Es wird NUR gedruckt, was angehakt ist!
        if fehler_berichte:
            for bericht in fehler_berichte:
                st.write(bericht)
        else:
            st.success("✨ Hervorragend! Es wurden keine akuten Formfehler für diese Pose protokolliert.")

        # Textfeld für das Protokoll
        st.text_area("Protokoll-Notiz für den Vortrag:", placeholder="Welche Fehler wurden heute besprochen?")
