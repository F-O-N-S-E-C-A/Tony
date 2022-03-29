import cv2

def drawBounds(img, points):
    if points is not None:
        for i in points:
            img_draw = cv2.rectangle(img, (int(i[0][0]), int(i[0][1])), (int(i[2][0]), int(i[2][1])), (0, 255, 0), 3)
        return img_draw

def readQR(img):
    det = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(img)
    return decoded_info, points

