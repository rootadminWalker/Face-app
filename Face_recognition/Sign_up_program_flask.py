import Recognize
import cv2
import os

um = Recognize.UsersManager()
fr = Recognize.FaceRecognizer()
cap = cv2.VideoCapture(0)
i = 0

while True:
	success, frame = cap.read()
	if not success:
		break

	um.show_face_image(frame)
	if not os.path.exists("cache/frame" + str(i) + ".jpg"):
		cv2.imwrite('cache/frame' + str(i) + ".jpg", frame)

	cv2.imshow("frame", frame)

	if cv2.waitKey(1) == ord('q'):
		break
	i += 1
um.sign_up("Thomas_Leong")
os.system("del /S /q cache")
