import socket
import requests
import time


def ping_ip(domain='8.8.8.8', port=80):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((domain, port))
        ip = s.getsockname()[0]
        s.close()
        name = socket.gethostname()
        return name, ip
    except Exception as e:
        print("Unable to send out your ip. The internet wasn't connected")
        return '', ''


try:
    name, ip = ping_ip()
    domain = "kinda.ktrackmp.com"
    url = "http://" + domain + "/rpi/rec.php"
    data = {}
    data['name'] = name
    data['ip'] = ip
    print(data)
    if ip != '':
        req = requests.get(url, data)
        print(req.text)
    time.sleep(30)

except Exception as e:
    print(e)
