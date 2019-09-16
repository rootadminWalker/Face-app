import dlib
import cv2
import pandas as pd
import numpy as np
import os

path = "./Users"
_shape_dat = "shape_predictor_68_face_landmarks.dat"
_face_dat = "dlib_face_recognition_resnet_model_v1.dat"

_detector = dlib.get_frontal_face_detector()
_predictor = dlib.shape_predictor(_shape_dat)
_recognizer = dlib.face_recognition_model_v1(_face_dat)
data = []
faces = []
face_name = []

for _, _, filenames in os.walk(path):
    for file in filenames:
        if file.endswith(".xlsx"):
            data = pd.read_excel("Users/" + file)
            desc = np.array(data.iloc[:, 1].values.tolist()).reshape(1, -1)[0]
            faces.append(desc)
            face_name.append(file)
print(faces)

cap = cv2.VideoCapture(0)
success = False
frame = None
shape = None
description = None

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
        description = np.array(_recognizer.compute_face_descriptor(frame, shape))
        for x in range(68):
            cv2.circle(frame, (shape.part(x).x, shape.part(x).y), 3, (0, 0, 255), 1)


    """
    writer = pd.ExcelWriter("description.xlsx", engine='xlsxwriter')
    data = pd.DataFrame(description)
    data.to_excel(writer, '128D', float_format='%.9f')
    writer.save()
    """
    if description is not None:
        for i, x in enumerate(faces):
            dist = np.sqrt(np.sum(np.square(description - x)))
            if dist < 0.4:
                print(face_name[i][0:-5])

    else:
        print("Nobody is here")

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

    success, frame = cap.read()

cap.release()
cv2.destroyAllWindows()

print("OK")
