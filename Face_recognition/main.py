from flask import *
import Recognize
import cv2
import Crawler
import os

path = "D:\\image_recognition_test\\images"
min = 0
i = 0
app = Flask(__name__)
um = Recognize.UsersManager()
s = Crawler.html("http://kinda.ktrackmp.com/rpi")
_URL = "http://" + Crawler.find(s, "<span id='RPi_Kinda'>", "</span>") + ":8540/username"

for _, _, filenames in os.walk(path):
    for file in filenames:
        number = int(file[:-4])
        if number > min:
            min = number

i = min + 1


@app.route("/", methods=['POST', "GET"])
def index():
    global i
    imagefile = request.files['media']
    print(imagefile)
    imagefile.save('temp.jpg')
    os.system("copy temp.jpg D:\\image_recognition_test\\images\\" + str(i) + ".jpg")

    image = cv2.cvtColor(cv2.imread('temp.jpg', cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

    username = um.sign_in(image)
    print(username)
    i += 1
    return username


if __name__ == '__main__':
    app.run(port=4000, debug=True, host="0.0.0.0")
