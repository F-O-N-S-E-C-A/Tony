import cv2 as cv
import numpy as np
from urllib.request import urlopen
import QR_reader
import requests
import threading
import time
import socket

'''
 -- ARDUINO COMMANDS --
LED_ON
LED_OFF
FOLLOW_LINE
STOP
LOOK_AROUND
STOP_LOOKING
HORIZONTAL_SERVO-100
VERTICAL_SERVO-100
'''

box1 = "ba721314-b4b8-11ec-ad41-acde48001122"
box2 = "ba6ddf56-b4b8-11ec-ad41-acde48001122"


url = 'http://192.168.4.4'
url_stream = url + ':81/stream'
url_cmd = url + '/action'



def cmd(str, url_cmd):
    print("Sent command: " + str)
    headers = {"Content-Type": "application/json; charset=utf-8",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
    myobj = {'go': bytes(str, 'ASCII')}
    x = requests.get(url_cmd, params=myobj, headers=headers)


def sendCommands_thread():
    cmd('VERTICAL_SERVO-60', url_cmd)

    while True:

        cmd('FOLLOW_LINE', url_cmd)
        time.sleep(6)
        cmd('STOP', url_cmd)

        cmd('LOOK_AROUND', url_cmd)
        time.sleep(5)
        cmd('STOP_LOOKING', url_cmd)
        cmd('STOP_LOOKING', url_cmd)
        cmd('HORIZONTAL_SERVO-90', url_cmd)


def find_box(box_id):

    x = threading.Thread(target=sendCommands_thread, args=())
    x.start()

    CAMERA_BUFFRER_SIZE = 4096
    stream = urlopen(url_stream)
    bts = b''
    i = 0

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

                if data is not None:
                    for d in data:
                        if d == box_id:
                            cmd("LED_ON", url_cmd)
                            time.sleep(0.5)
                            cmd("LED_OFF", url_cmd)

                            print("Box Found!!")

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

    cv.destroyAllWindows()


def main():
    find_box(box1)


if __name__ == "__main__":
    main()