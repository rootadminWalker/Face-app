import dlib
import cv2
import pandas as pd
import numpy as np
import os

username = input("Who are you? ")
if os.path.exists("./Users/" + username + ".xlsx"):
    print("This user has already exist!")
else:
    pass

_shape_dat = "shape_predictor_68_face_landmarks.dat"
_face_dat = "dlib_face_recognition_resnet_model_v1.dat"

_detector = dlib.get_frontal_face_detector()
_predictor = dlib.shape_predictor(_shape_dat)
_recognizer = dlib.face_recognition_model_v1(_face_dat)

cap = cv2.VideoCapture(0)
success = False
frame = None
shape = None
if cap.isOpened():
    success, frame = cap.read()

while success:
    dets, scores, orientations = _detector.run(frame, False)
    for i, d in enumerate(dets):
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        shape = _predictor(frame, d)
        for x in range(68):
            cv2.circle(frame, (shape.part(x).x, shape.part(x).y), 3, (0, 0, 255), 1)

    description = np.array(_recognizer.compute_face_descriptor(frame, shape))
    writer = pd.ExcelWriter("./Users/" + username + ".xlsx", engine='xlsxwriter')
    data = pd.DataFrame(description)
    data.to_excel(writer, '128D', float_format='%.9f')
    writer.save()

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

    success, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

print("OK")
