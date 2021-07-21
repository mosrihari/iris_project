import cv2
import eye_aspect_ratio
import mediapipe as mp
from playsound import playsound

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
thresh = 0.18
flag = 0
frames = 20

font = cv2.FONT_HERSHEY_SIMPLEX
# org
org1 = (50, 50)
org2 = (75,75)
# fontScale
fontScale = 1
# Blue color in BGR
color1 = (255, 0, 0)
color2 = (0,0, 255)
thickness = 2

with mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACE_CONNECTIONS,
        #     landmark_drawing_spec=drawing_spec,
        #     connection_drawing_spec=drawing_spec)
        left_eye_array = [[face_landmarks.landmark[161].x, face_landmarks.landmark[161].y],
                          [face_landmarks.landmark[163].x, face_landmarks.landmark[163].y],
                          [face_landmarks.landmark[157].x, face_landmarks.landmark[157].y],
                          [face_landmarks.landmark[154].x, face_landmarks.landmark[154].y],
                          [face_landmarks.landmark[33].x, face_landmarks.landmark[33].y],
                          [face_landmarks.landmark[133].x, face_landmarks.landmark[133].y]]
        right_eye_array = [[face_landmarks.landmark[384].x, face_landmarks.landmark[384].y],
                          [face_landmarks.landmark[381].x, face_landmarks.landmark[381].y],
                          [face_landmarks.landmark[388].x, face_landmarks.landmark[388].y],
                          [face_landmarks.landmark[390].x, face_landmarks.landmark[390].y],
                          [face_landmarks.landmark[362].x, face_landmarks.landmark[362].y],
                          [face_landmarks.landmark[263].x, face_landmarks.landmark[263].y]]
        left_ear = eye_aspect_ratio.ear(left_eye_array)
        right_ear = eye_aspect_ratio.ear(right_eye_array)
        ear = (left_ear + right_ear) / 2.0
        cv2.putText(image, 'EAR:' + str(ear), org1, font, fontScale, color1, thickness, cv2.LINE_AA)
        if(ear < thresh):
            flag += 1
            if(flag >= 20):
                cv2.putText(image, 'ALERT DROWSY' , org2, font,fontScale, color2, thickness, cv2.LINE_AA)
                # playsound("")
                flag = 0
        else:
            flag = 0
    cv2.imshow('MediaPipe FaceMesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

