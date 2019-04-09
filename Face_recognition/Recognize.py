import dlib
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime


class UsersManager:
    def __init__(self):
        self.fr = FaceRecognizer()
        self.averge_value = list()

    def sign_up(self, name, image):
        description, dets = self.fr.calculate_128D(image)
        self.fr.draw_128D(image, dets)
        if len(description) > 0:
            writer = pd.ExcelWriter("./Users/" + name + ".xlsx", engine='xlsxwriter')
            data = pd.DataFrame(description[0])
            data.to_excel(writer, '128D', float_format='%.9f')
            writer.save()

    def sign_in(self, image):
        users = self.get_user()
        desc, dets = self.fr.calculate_128D(image)
        if len(desc) > 0:
            self.fr.draw_128D(image, dets)
            for key, val in users.items():
                if self.fr.recognize_user(val, desc[0]):
                    return key

        return ''

    def get_user(self):
        users = dict()
        for f in os.listdir("Users"):
            if f.endswith(".xlsx"):
                data = pd.read_excel("Users/" + f)
                desc = np.array(data.iloc[:, 1].values.tolist()).reshape(1, -1)[0]
                users[f[:-5]] = desc
        return users

    def load_cache(self):
        for _, _, filenames in os.walk("cache"):
            for cache in filenames:
                cache_image = cv2.cvtColor(cv2.imread('cache/' + cache, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
                description, _ = self.fr.calculate_128D(cache_image)
                self.averge_value.append(description)
        try:
            return np.average(self.averge_value, axis=1)
        except IndexError:
            return []


class FaceRecognizer:
    def __init__(self):
        _shape_dat = "lib/shape_predictor_68_face_landmarks.dat"
        _face_dat = "lib/dlib_face_recognition_resnet_model_v1.dat"

        self._detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(_shape_dat)
        self._recognizer = dlib.face_recognition_model_v1(_face_dat)

    def calculate_128D(self, image):
        descriptions = list()
        dets, _, _ = self._detector.run(image, False)
        for d in dets:
            shape = self._predictor(image, d)
            description = np.array(self._recognizer.compute_face_descriptor(image, shape))
            descriptions.append(description)
        return descriptions, dets

    def recognize_user(self, d1, d2):
        dist = np.sqrt(np.sum(np.square(d1 - d2)))
        return dist < 0.4

    def draw_128D(self, image, dets):
        for i, d in enumerate(dets):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            shape = self._predictor(image, d)
            for x in range(68):
                cv2.circle(image, (shape.part(x).x, shape.part(x).y), 3, (0, 0, 255), 1)


def show_info(*args):
    for arg in args:
        text = ''.join(arg)
        print("[INFO@" + str(datetime.today()) + "*]" + text)


if __name__ == '__main__':
    show_info("Preparing dlib")
    um = UsersManager()
    fr = FaceRecognizer()
    show_info("Finding camera")
    cap = cv2.VideoCapture(0)
    show_info("Camera found")
    show_info("Opening camera for recognition")
    i = 0
    while True:
        success, frame = cap.read()
        if not success:
            show_info("There is an error when reading the camera, Please check your camera or the security settings")
            break
        show_info("Recognize person: " + str(um.sign_in(frame)))
        cv2.imshow("frame", frame)
        if not os.path.exists("cache/frame" + str(i) + ".jpg"):
            cv2.imwrite('cache/frame' + str(i) + ".jpg", frame)
        else:
            pass

        if cv2.waitKey(1) == ord('q'):
            os.system("del /S /q cache")
            break
        i += 1