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
    
    # Hier stand der Fehler: Jetzt ist alles sauber in einer Zeile berechnet!
    basis_score = (score_kopf + score_arm + score_fuss) / 3
    
    # KNALLHARTES ABZUGSSYSTEM
    abzug = 0
    kritik_punkte = []
    
    if fehler_drehung:
        abzug += 30
        kritik_punkte.append("🛑 **Achsen-Kollaps:** Du stehst nicht über deinem Standbein und bist aus der Drehung gefallen. Ohne Körperspannung im Core (Bauch/Rücken) bleibt jede Pirouette instabil.")
    
    if fehler_spotten:
        abzug += 25
        kritik_punkte.append("🛑 **Kopf-Verzögerung:** Kein Spotting sichtbar! Wenn der Blick den Fixpunkt verliert und der Kopf nicht peitschenknallartig dreht, verlierst du die Orientierung.")
        
    if fehler_banane:
        abzug += 25
        kritik_punkte.append("🛑 **Bananenfuß:** Unsaubere Fußstreckung! Das Fußgelenk knickt ein. Die Zehen müssen aktiv langgezogen werden, um eine Linie mit dem Schienbein zu bilden.")

    # Berechne das finale Ergebnis
    gesamtscore = basis_score - abzug
    
    # Der Ballettmeister-Trick: Es gibt niemals 100%!
    if gesamtscore > 95:
        gesamtscore = 92.5
    
    st.divider()
    st.header("📋 Das Urteil des Ballettmeisters")
    
    col_fb1, col_fb2 = st.columns(2)
    
    with col_fb1:
        st.subheader("📊 Unerbittliche Punktebewertung")
        
        if gesamtscore >= 85:
            st.warning(f"⚠️ {gesamtscore:.1f}% – Sauberer Ansatz, ABER weit entfernt von Perfektion. Es fehlt an Leichtigkeit und korrekter Körperspannung.")
        elif gesamtscore >= 60:
            st.error(f"❌ {gesamtscore:.1f}% – Mangelhafte Ausführung! Grobe Defizite in der Platzierung des Körpers.")
        else:
            st.error(f"💀 {gesamtscore:.1f}% – Inakzeptabel! Gehe zurück an die Stange (Barre) und arbeite an deiner Basis-Platzierung.")

        st.write("**Detaillierte Abweichungen:**")
        st.write(f"- Kopf-Präzision: {score_kopf:.1f}%")
        st.write(f"- Arm-Linie (Port de bras): {score_arm:.1f}%")
        st.write(f"- Fuß-Spannung (Extension): {score_fuss:.1f}%")
            
    with col_fb2:
        st.markdown("### 📝 Unverzügliche Korrektur-Aufgaben")
        
        if kritik_punkte:
            for kritik in kritik_punkte:
                st.write(kritik)
        
        st.markdown("---")
        st.markdown("##### 🩰 Mikro-Korrekturen (Die immer gelten):")
        st.write("• **Schultern:** Drücke die Schulterblätter aktiv nach unten! Sie wandern viel zu weit zu den Ohren.")
        st.write("• **Finger:** Die Hände wirken verkrampft. Die Finger müssen die Bewegung weich verlängern.")
        st.write("• **Standbein:** Das Knie des Standbeins ist nicht maximal durchgestreckt!")

        st.text_area("Eigenanalyse für das Vortragsprotokoll:", placeholder="Welche Korrekturhinweise des Lehrers wurden heute umgesetzt?")
