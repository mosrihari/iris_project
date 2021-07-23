import cv2
import mediapipe as mp
import distance_from_camera
from document_access import word_access

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color1 = (255, 0, 0)
thickness = 2
known_width = 7.62 # width between eyes approx (in cm)
known_distance = 24
known_focal_length = 50
thresh = 1350

with mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        eye_corners = [[face_landmarks.landmark[33].x, face_landmarks.landmark[33].y],
                          [face_landmarks.landmark[263].x, face_landmarks.landmark[263].y]]
        pixel = distance_from_camera.pixel_width(eye_corners, known_focal_length, known_width, known_distance)
        #focal_length = distance_from_camera.focal_length(known_width, pixel)
        distance_offset = distance_from_camera.calculate_distance(known_focal_length,
                                                                  known_width,
                                                                  pixel)
        distance = distance_offset + known_distance
        cv2.putText(image, 'distance:' + str(distance), org, font, fontScale, color1, thickness, cv2.LINE_AA)
        word_object = word_access.run()
        if(word_object != -1):
            return_value = word_access.increase_font_size(word_object,distance,thresh)
        else:
            break
    cv2.imshow('Focal Length Detection', image)
    # if((return_value == -1) or (word_object == -1)):
    #   break
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()