import mediapipe as mp
import cv2
import numpy as np
import pyautogui
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks = True)
screen_w,screen_h = pyautogui.size()
cap = cv2.VideoCapture(0) 
while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        break
    frame=cv2.flip(frame,1)
    frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=face_mesh.process(frame_rgb)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = face_landmarks.landmark[145]
            x,y=int(left_eye.x*screen_w),int(left_eye.y*screen_h)
            pyautogui.moveTo(x,y)
    cv2.imshow("Eye cursor - Move Mouse with Eyes",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()