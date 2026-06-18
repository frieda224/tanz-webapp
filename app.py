import streamlit as st
from PIL import Image

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Ballett-Akademie Analyse tool", layout="wide")

st.title("🩰 Akademisches Ballett-Analyse-Protokoll")
st.write("Eine unbestechliche Auswertung für die präzise Korrektur von Tanzhaltungen.")

# --- BILDER HOCHLADEN ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Profi-Referenz (Soll-Form)")
    profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")
    if profi_file:
        profi_img = Image.open(profi_file)
        st.image(profi_img, caption="Perfekte Platzierung des Profis", use_container_width=True)

with col2:
    st.subheader("2. Deine Ausführung (Ist-Form)")
    user_file = st.file_uploader("Dein Foto hochladen", type=["jpg", "png", "jpeg"], key="user")
    if user_file:
        user_img = Image.open(user_file)
        st.image(user_img, caption="Deine Pose zur harten Bewertung", use_container_width=True)

# --- STRENGE UND SPEZIFISCHE BALLETT-ANALYSE ---
if profi_file and user_file:
    st.divider()
    st.header("🔍 Protokollierung spezifischer Haltungsmängel")
    st.write("Hake exakt die Fehler an, die auf deinem Foto zu sehen sind. Die KI berechnet die Wertung knallhart.")
    
    col_links, col_rechts = st.columns(2)
    
    # Hier werden die Fehlerpunkte und Texte gesammelt
    punktabzug = 0
    fehler_berichte = []
    
    with col_links:
        st.markdown("### 👤 Kopf & Oberkörper")
        
        # Fehler 1: Spotting
        spotten_fehler = st.checkbox("❌ Kopf spottet nicht / Blick verloren", key="chk_spotten")
        if spotten_fehler:
            punktabzug += 25
            fehler_berichte.append("🛑 **Spotting-Defizit:** Der Kopf verzögert in der Drehung. Ohne fixierten Fokus geht die Orientierung und die saubere Dynamik der Pirouette verloren.")
            
        # Fehler 2: Schultern
        schulter_fehler = st.checkbox("❌ Schultern hochgezogen (Verkrampfung)", key="chk_schulter")
        if schulter_fehler:
            punktabzug += 15
            fehler_berichte.append("🛑 **Schulter-Platzierung:** Die Schultern wandern zu den Ohren. Drücke die Schulterblätter aktiv nach unten, um die Halslinie (Port de bras) zu wahren.")

        st.markdown("### 💪 Arme & Hände")
        
        # Fehler 3: Ellbogen
        ellbogen_fehler = st.checkbox("❌ Ellbogen hängen durch / Keine runde Form", key="chk_ellbogen")
        if ellbogen_fehler:
            punktabzug += 15
            fehler_berichte.append("🛑 **Arm-Geometrie:** Die Ellbogen fallen ab. Im Ballett halten die Arme eine stolze, getragene, runde Form (wie ein großer Kreis vor dem Körper).")

    with col_rechts:
        st.markdown("### 🦵 Beine & Stand")
        
        # Fehler 4: Achse verloren
        achse_fehler = st.checkbox("❌ Aus der Drehung gefallen / Achse verloren", key="chk_achse")
        if achse_fehler:
            punktabzug += 30
            fehler_berichte.append("🛑 **Achsen-Kollaps:** Du stehst nicht zentriert über dem Standbein. Der Core (Bauch/Rücken) muss maximal stabilisiert werden, um das Gleichgewicht zu halten.")

        st.markdown("### 🩰 Füße (Spezifische Abfrage)")
        
        # Fehler 5: Der Bananenfuß – taucht NUR auf, wenn hier angehakt!
        bananen_fehler = st.checkbox("❌ Bananenfuß (Unsaubere, eingeknickte Fußstreckung)", key="chk_banane")
        if bananen_fehler:
            punktabzug += 25
            fehler_berichte.append("🛑 **Bananenfuß:** Unsaubere Fußstreckung! Das Gelenk bricht in der Spitze ein. Du musst die Zehen aktiv in einer fließenden, verlängerten Linie zum Schienbein herausstrecken.")

    # --- BEWERTUNG BERECHNEN ---
    # Wir starten bei 100 Punkten. Jeder angehakte Fehler zieht massiv Punkte ab.
    maximal_score = 100
    finaler_score = maximal_score - punktabzug
    
    # Im Ballett ist nie etwas absolut perfekt – kleine Deckelung, wenn kein Fehler angehakt ist
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
            st.warning(f"⚠️ {finaler_score:.1f}% – Befriedigend. Die Grundform ist sauber, aber feine Nuancen der Körperspannung müssen weiter trainiert werden.")
        elif finaler_score >= 60:
            st.error(f"❌ {finaler_score:.1f}% – Mangelhaft! Erhebliche technische Defizite. Die markierten Fehler verhindern eine saubere Ausführung.")
        else:
            st.error(f"💀 {finaler_score:.1f}% – Ungenügend! Abbruch der Bewertung. Gehe zurück an die Stange (Barre) und arbeite strikt an den Grundlagen.")
            
    with col_res2:
        st.markdown("### 📝 Spezifische Korrektur-Anweisungen")
        
        if fehler_berichte:
            for bericht in fehler_berichte:
                st.write(bericht)
        else:
            st.success("✨ Keine akuten Formfehler für die ausgewählten Bereiche protokolliert. Achte weiterhin auf maximale Streckung des Standbeins und weiche Fingerhaltung.")

        # Textfeld für das eigene Vortragsprotokoll
        st.text_area("Protokoll-Notiz für den Vortrag:", placeholder="Welche Fortschritte wurden erzielt? Welche Korrektur hat am meisten geholfen?")
