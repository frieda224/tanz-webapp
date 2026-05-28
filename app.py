import sys
# Trick: Wir zwingen Python, die Headless-Version als Standard-OpenCV zu akzeptieren
import cv2
sys.modules['cv2'] = cv2

import streamlit as st
import numpy as np
from PIL import Image
import mediapipe as mp
import math

# --- SEITEN-SETUP ---
st.set_page_config(page_title="Tanz-Trainer KI", layout="wide")

st.title("🩰 Tanz-Trainer KI")
st.write("Vergleiche deine Pose mit einem Profi. Komplett stabil ohne Abstürze!")

# --- MEDIAPIPE INITIALISIEREN ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# --- HILFSFUNKTION: WINKEL BERECHNEN ---
def calculate_angle(a, b, c):
    """Berechnet den Winkel zwischen drei Gelenkpunkten (Schulter, Ellenbogen, Handgelenk)"""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

# --- BILDER HOCHLADEN ---
st.subheader("1. Referenz-Pose des Profis")
profi_file = st.file_uploader("Profi-Foto hochladen", type=["jpg", "png", "jpeg"], key="profi")

st.subheader("2. Dein Foto")
user_file = st.file_uploader("Lade dein eigenes Foto hoch", type=["jpg", "png", "jpeg"], key="user")

if profi_file and user_file:
    # Bilder vorbereiten
    profi_img = Image.open(profi_file).convert('RGB')
    user_img = Image.open(user_file).convert('RGB')
    
    profi_cv = np.array(profi_img)
    user_cv = np.array(user_img)
    
    # KI-Verarbeitung (Modell berechnet das Skelett)
    res_profi = pose.process(profi_cv)
    res_user = pose.process(user_cv)
    
    profi_draw = profi_cv.copy()
    user_draw = user_cv.copy()
    
    # Prüfen, ob Personen erkannt wurden
    if res_profi.pose_landmarks and res_user.pose_landmarks:
        # Skelett-Linien auf die Bilder zeichnen
        mp_drawing.draw_landmarks(profi_draw, res_profi.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(user_draw, res_user.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Nebeneinander anzeigen
        col1, col2 = st.columns(2)
        with col1:
            st.image(profi_draw, caption="Profi-Pose (Analysiert)", use_container_width=True)
        with col2:
            st.image(user_draw, caption="Deine Pose (Analysiert)", use_container_width=True)
            
        # Gelenkpunkte auslesen
        kp_profi = res_profi.pose_landmarks.landmark
        kp_user = res_user.pose_landmarks.landmark
        
        # Winkel berechnen (Beispiel: Rechter Ellenbogen)
        # Punkte-IDs bei MediaPipe: Schulter (12), Ellenbogen (14), Handgelenk (16)
        winkel_profi = calculate_angle(kp_profi[12], kp_profi[14], kp_profi[16])
        winkel_user = calculate_angle(kp_user[12], kp_user[14], kp_user[16])
        
        # Score berechnen (100 minus die Abweichung der Winkel)
        unterschied = abs(winkel_profi - winkel_user)
        score = max(0, 100 - unterschied)
        
        # --- FEEDBACK AUSGABE ---
        st.divider()
        st.header("📋 KI-Auswertung")
        
        if score > 85:
            st.success(f"🌟 Sensationell! Deine Haltung stimmt zu {score:.1f}% mit dem Profi überein!")
        elif score > 60:
            st.warning(f"👍 Solide Leistung! Übereinstimmung: {score:.1f}%. Korrigiere deinen Armwinkel leicht.")
        else:
            st.error(f"❌ Übereinstimmung: {score:.1f}%. Schau dir den Winkel im Profibild noch einmal genau an.")
            
        st.info(f"Winkel beim Profi: {winkel_profi:.1f}° | Dein Winkel: {winkel_user:.1f}°")
        
    else:
        st.error("Die KI konnte keine Körperhaltungen berechnen. Bitte lade Bilder hoch, auf denen die Personen komplett zu sehen sind!")
