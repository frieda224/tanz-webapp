import streamlit as st
from PIL import Image
import cv2
import mediapipe as mp
import numpy as np

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Anatomische Ballett-Analyse", layout="wide")

st.title("🩰 Anatomisches Ballett-Analyse-Protokoll")
st.write("Echte Gelenk- und Achsenberechnung über Computer Vision. Erkennt Fehler basierend auf Biomechanik.")

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
        st.image(user_img, caption="Deine Pose zur anatomischen Analyse", use_container_width=True)

# --- WINKELBERECHNUNG (MATHEMATISCH) ---
def berechne_winkel(a, b, c):
    a = np.array(a) # Punkt A (z.B. Hüfte)
    b = np.array(b) # Punkt B (z.B. Knie / Scheitelpunkt)
    c = np.array(c) # Punkt C (z.B. Knöchel)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    winkel = np.abs(radians*180.0/np.pi)
    
    if winkel > 180.0:
        winkel = 360-winkel
        
    return winkel

# --- ECHTE BILDVERARBEITUNG MIT MEDIAPIPE ---
if profi_file and user_file:
    st.divider()
    
    # MediaPipe Pose-Erkennung initialisieren
    mp_pose = mp.solutions.pose
    
    with st.spinner("Extrahiere Skelettachsen und berechne Gelenkwinkel..."):
        # Konvertiere das User-Bild für OpenCV
        user_cv = cv2.cvtColor(np.array(user_img), cv2.COLOR_RGB2BGR)
        
        with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            ergebnis = pose.process(cv2.cvtColor(user_cv, cv2.COLOR_BGR2RGB))
            
            if not ergebnis.pose_landmarks:
                st.error("🛑 Es wurden keine Gelenke auf deinem Foto erkannt. Bitte achte darauf, dass dein ganzer Körper gut sichtbar ist!")
            else:
                landmarks = ergebnis.pose_landmarks.landmark
                
                # Koordinaten wichtiger Gelenke auslesen (normalisiert von 0 bis 1)
                schulter_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                huefte_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knie_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                knoechel_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                zeh_l = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                
                # --- BIOMECHANISCHE ANALYSE ---
                fehler_berichte = []
                score = 100
                
                # 1. Kniebeugung berechnen (Wie tief ist das Plié?)
                knie_winkel = berechne_winkel(huefte_l, knie_l, knoechel_l)
                
                # 2. Oberkörper-Lot prüfen (Hüft-Schulter-Winkel zur Vertikalen)
                oberkoerper_winkel = berechne_winkel([huefte_l[0], 0], huefte_l, schulter_l)
                
                # 3. Fußstreckungs-Achse (Winkel zwischen Knie, Knöchel und Zehenspitze)
                fuss_winkel = berechne_winkel(knie_l, knoechel_l, zeh_l)
                
                # --- FEHLERDEFINITION BASIEREND AUF MESSWERTEN ---
                
                # Überprüfung des Oberkörpers (Darf beim Plié nicht nach vorne kippen)
                if oberkoerper_winkel > 12:
                    score -= 25
                    fehler_berichte.append(f"🛑 **Oberkörper kippt vor ({oberkoerper_winkel:.1f}° Abweichung):** Beim Plié muss das Becken zentriert und der Rücken vollkommen vertikal bleiben. Du verlagerst das Gewicht fälschlicherweise nach vorne.")
                
                # Überprüfung auf Bananenfuß (Wenn das Bein gestreckt sein sollte, oder die Fußachse einknickt)
                # Ein blockiertes oder falsch auswärts gedrehtes Gelenk verändert den Winkel zwischen Knie und Zeh
                if fuss_winkel < 130 and knie_winkel > 160: 
                    score -= 25
                    fehler_berichte.append(f"🛑 **Bananenfuß / Unsaubere Fußachse ({fuss_winkel:.1f}°):** Bei gestrecktem Bein bricht die Linie zum Spann ein. Die Zehen verlängern nicht die Linie des Schienbeins.")
                
                # Warnung, falls überhaupt keine Kniebeugung stattfindet (Kein echtes Plié)
                if knie_winkel > 172:
                    fehler_berichte.append(f"ℹ️ **Hineinzoomen auf Knieachse:** Dein Standbein ist fast vollständig gestreckt ({knie_winkel:.1f}°). Für ein Plié ist keine ausreichende Beugung messbar.")

                score = max(0, score)
                
                # --- AUSGABE DES URTEILS ---
                st.header("📋 Das Urteil der anatomischen Auswertung")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.subheader("📊 Gemessene Winkelwerte")
                    st.write(f"- **Knie-Beugung:** {knie_winkel:.1f}°")
                    st.write(f"- **Oberkörper-Lot:** {oberkoerper_winkel:.1f}°")
                    st.write(f"- **Fußgelenk-Linie:** {fuss_winkel:.1f}°")
                    
                    st.metric(label="Gesamtnote der Körperplatzierung", value=f"{score:.1f}%")
                    
                with col_res2:
                    st.markdown("### 📝 Reales Mängelprotokoll")
                    if fehler_berichte:
                        for bericht in fehler_berichte:
                            st.write(bericht)
                    else:
                        st.success("✨ Die Gelenkachsen entsprechen der anatomischen Vorgabe für diese Position. Keine groben Fehlstellungen in Oberkörper oder Fußgelenk detektiert.")
