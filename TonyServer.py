import cv2 as cv
import numpy as np
from urllib.request import urlopen
import QR_reader
import requests
import threading
import time
import socket
import speech_recognition as sr

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
PORT = 1999  # Server port

boxes = {"fruit": "ba721314-b4b8-11ec-ad41-acde48001122",
         "vodka": "ba683fec-b4b8-11ec-ad41-acde48001122",
         "whiskey": "ba6ddf56-b4b8-11ec-ad41-acde48001122",
         "pizza": "ba6f4346-b4b8-11ec-ad41-acde48001122",
         "arduino components": "ba70a89e-b4b8-11ec-ad41-acde48001122",
         "donut": "ba74fc46-b4b8-11ec-ad41-acde48001122"}


url = 'http://192.168.4.2'
url_stream = url + ':81/stream'
url_cmd = url + '/action'

class SearchMovement:

    def __init__(self):
        self.__running = True

    def terminate(self):
        self.__running = False

    def run(self):
        cmd('VERTICAL_SERVO-60', url_cmd)

        while self.__running:
            cmd('FOLLOW_LINE', url_cmd)
            time.sleep(6)
            cmd('STOP', url_cmd)

            cmd('LOOK_AROUND', url_cmd)
            time.sleep(5)
            cmd('STOP_LOOKING', url_cmd)
            cmd('STOP_LOOKING', url_cmd)
            cmd('HORIZONTAL_SERVO-90', url_cmd)


def serve():
    print("Server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    data = data.decode("utf-8").split(":")
                    print(data)
                    if data[0] == "FIND":
                        id = data[1]
                        print("Find box with id: ", id)
                        if find_box(box_id=id) == 0:
                            response = "BOX_FOUND:" + id
                            print(response)
                            #conn.sendall(response.encode())
                    elif data[0] == "VOICE_RECOGNITION":
                        text = speech_recognition()
                        text.strip().lower()
                        print(text)
                        if text in boxes.keys():
                            id = boxes.get(text)
                            if find_box(box_id=id) == 0:
                                response = "BOX_FOUND:" + id
                                print(response)
                                #conn.sendall(response.encode())
                        else:
                            response = "BOX_NOT_AVAILABLE:" + id
                            print(response)
                            #conn.sendall(response.encode())
                        print("over")


def speech_recognition():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        return r.recognize_google(audio)


def cmd(str, url_cmd):
    print("Sent command: " + str)
    headers = {"Content-Type": "application/json; charset=utf-8",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
    myobj = {'go': bytes(str, 'ASCII')}
    x = requests.get(url_cmd, params=myobj, headers=headers)


def find_box(box_id):

    search_movement = SearchMovement()
    thread_sm = threading.Thread(target=search_movement.run, args=())
    thread_sm.start()

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
                            if d == box_id:
                                cmd("LED_ON", url_cmd)
                                time.sleep(0.5)
                                cmd("LED_OFF", url_cmd)

                                search_movement.terminate()
                                thread_sm.join()

                                cmd('FOLLOW_LINE', url_cmd)
                                cmd('STOP_AT_CHECKPOINT', url_cmd)

                                print("Box Found!!")

                                return 0

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
    serve()
    #find_box(box_id=boxes["pizza"])


if __name__ == "__main__":
    main()