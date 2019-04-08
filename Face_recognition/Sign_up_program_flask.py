import Recognize
import cv2

username = input("Who are you? ")
print("Always press q in the camera window to exit")

Recognize.show_info("Preparing dlib")
um = Recognize.UsersManager()
fr = Recognize.FaceRecognizer()
Recognize.show_info("Finding camera")
cap = cv2.VideoCapture(0)
Recognize.show_info("Camera found")
Recognize.show_info("Opening camera for recognition")

while True:
	success, frame = cap.read()
	if not success:
		Recognize.show_info("There is an error when reading the camera, Please check your camera or the security settings")
		break
	um.sign_up(username, frame)
	cv2.imshow("frame", frame)

	if cv2.waitKey(1) == ord('q'):
		break
