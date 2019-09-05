#!/usr/bin/python3
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

    def sign_in(self, image):
        # result = list()
        most_common_element = int(0)
        users = self.get_user()
        desc, dets = self.fr.calculate_128D(image)
        if len(desc) > 0:
            self.fr.draw_128D(image, dets)

            for key, val in users.items():
                result = list()
                for landmarks in val:
                    result.append(int(self.fr.recognize_user(landmarks, desc[0])))
                    final_result = np.bincount(result)
                    most_common_element = np.argmax(final_result)


                if most_common_element:
                    return key

        return ''

    def get_user(self):
        users = dict()
        # all_description = list()
        for f in os.listdir("Users"):
            user_base = os.listdir(os.path.join("Users", f))
            all_description = list()
            for user in user_base:
                data = pd.read_excel("Users/" + f + os.sep + user)
                desc = np.array(data.iloc[:, 1].values.tolist()).reshape(1, -1)[0]
                all_description.append(desc)
                users[f] = all_description
        return users

    def sign_up(self, username):
        print("Loading cache...")
        for _, _, filenames in os.walk("cache"):
            for cache in filenames:
                cache_image = cv2.cvtColor(cv2.imread('cache/' + cache, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
                print("Loaded cache: {}".format(cache))
                description, _ = self.fr.calculate_128D(cache_image)
                print("Calculated cache: {}".format(cache))
                if len(description) > 0:
                    self.averge_value.append(description)

        print("Start calculating...")
        all_data = np.array(self.averge_value)
        print("All value --> ", all_data)
        if not os.path.isdir("./Users/" + username):
            os.mkdir("./Users/" + username)

        i = 0
        for desc in all_data:
            writer = pd.ExcelWriter("./Users/" + username + os.sep + username + str(i) + ".xlsx", engine='xlsxwriter')
            data = pd.DataFrame(desc[0])
            data.to_excel(writer, '128D', float_format='%.9f')
            writer.save()
            i += 1

class FaceRecognizer:
    def __init__(self):
        _shape_dat = "./lib/shape_predictor_68_face_landmarks.dat"
        _face_dat = "./lib/dlib_face_recognition_resnet_model_v1.dat"

        self._detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(_shape_dat)
        self._recognizer = dlib.face_recognition_model_v1(_face_dat)

    def show_face_image(self, image):
        description, dets = self.calculate_128D(image)
        self.draw_128D(image, dets)

    def calculate_128D(self, image):
        descriptions = list()
        dets, _, _ = self._detector.run(image, False)
        for d in dets:
            shape = self._predictor(image, d)
            description = np.array(self._recognizer.compute_face_descriptor(image, shape))
            descriptions.append(description)
        return np.array(descriptions), dets

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
            show_info("Clearing cache")
            os.system("rm -rf cache/*")
            break
        i += 1

    print("HI")
    cap.grab()
    cap.release()
    cv2.destroyAllWindows()
