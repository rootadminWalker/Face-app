from flask import *
import Recognize
import cv2
import os
from flask_cors import CORS

path = "D:\\image_recognition_test\\images"
min = 0
i = 0
app = Flask(__name__)

um = Recognize.UsersManager()
_new_username = ""
# s = Crawler.html("http://kinda.ktrackmp.com/rpi")
# _URL = "http://" + Crawler.find(s, "<span id='RPi_Kinda'>", "</span>") + ":8540/username"

for _, _, filenames in os.walk(path):
    for file in filenames:
        number = int(file[:-4])
        if number > min:
            min = number

i = min + 1


x = 0


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


@app.route("/collect_data", methods=['POST', 'GET'])
def add_account():
    global x, _new_username
    image = request.files['media']
    image.save("temp.jpg")
    image = cv2.imread("temp.jpg", cv2.IMREAD_COLOR)
    
    if not os.path.exists("./cache/frame" + str(x) + ".jpg"):
        cv2.imwrite('./cache/frame' + str(x) + ".jpg", image)
        x += 1

    return "Ok"


@app.route("/request_new_user", methods=["POST", 'GET'])
def request_new_user():
    global _new_username
    _new_username = request.form['new_user']
    print(_new_username)
    return _new_username


@app.route("/start_adding_user", methods=["POST", "GET"])
def start_adding_user():
    global _new_username, x
    um.sign_up(_new_username)
    os.system("rm -rf ./cache/*")
    x = 0
    return "true"


if __name__ == '__main__':
    app.run(port=4000, debug=True, host="0.0.0.0")
    CORS(app)
