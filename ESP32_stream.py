import cv2 as cv
import numpy as np
from urllib.request import urlopen
import QR_reader
import requests
import threading
import time

url = 'http://192.168.4.2'
url_stream = url + ':81/stream'
url_cmd = url + '/action'


def sendCommand(str, url_cmd):
    print("send cmd")
    headers = {"Content-Type": "application/json; charset=utf-8",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
    myobj = {'go': bytes(str, 'ASCII')}
    x = requests.get(url_cmd, params=myobj, headers=headers)

def sendCommands_thread():
    while True:
        for i in range(5, 165):
            CMD = "SERVO_HORIZONTAL-" + str(i)
            sendCommand(CMD, url_cmd)
            time.sleep(0.01)
        for i in range(165, 5, -1):
            CMD = "SERVO_HORIZONTAL-" + str(i)
            sendCommand(CMD, url_cmd)
            time.sleep(0.01)




x = threading.Thread(target=sendCommands_thread, args=())
x.start()

CAMERA_BUFFRER_SIZE = 4096
stream = urlopen(url_stream)
bts = b''
i = 0
count = 0
while True:
    try:
        bts += stream.read(CAMERA_BUFFRER_SIZE)
        jpghead = bts.find(b'\xff\xd8')
        jpgend = bts.find(b'\xff\xd9')
        if jpghead > -1 and jpgend > -1:
            jpg = bts[jpghead:jpgend + 2]
            bts = bts[jpgend + 2:]
            frame = cv.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED)

            data, points = QR_reader.readQR(frame) #QR content and position on image
            print(data)
            if (points is not None) and len(points) > 0:
                sendCommand("STOP", url_cmd)
                print("STOP")

            QR_reader.drawBounds(frame, points)

            cv.imshow("a", frame)
        k = cv.waitKey(1)
    except Exception as e:
        print("Error:" + str(e))
        bts = b''
        stream = urlopen(url_stream)
        continue

    k = cv.waitKey(1)
    if k & 0xFF == ord('a'):
        cv.imwrite(str(i) + ".jpg", frame)
        i = i + 1

    if k & 0xFF == ord('q'):
        break

    count +=1

    if count % 100 == 0:
        sendCommand("FOLLOW_LINE", url_cmd)


cv.destroyAllWindows()