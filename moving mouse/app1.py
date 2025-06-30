import mediapipe as mp
import cv2
import numpy as np
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) 
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    results = hands.process(frame_rgb)  

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[8] 
            
            x, y = int(index_finger_tip.x * screen_w), int(index_finger_tip.y * screen_h)
            
        
            pyautogui.moveTo(x, y)

    cv2.imshow("Hand Cursor - Move Mouse with Finger", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
