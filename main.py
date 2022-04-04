import cv2
import QR_reader

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()

    data, points = QR_reader.readQR(frame)
    print(data)

    QR_reader.drawBounds(frame, points)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()