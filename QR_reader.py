import cv2


def draw(img, points):
    for i in points:
        img_draw = cv2.rectangle(img, (int(i[0][0]), int(i[0][1])), (int(i[2][0]), int(i[2][1])), (0, 255, 0), 3)

    cv2.imshow("img", img_draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread("qr_phone.png")
det = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(img)

print('position: ', points)

draw(img, points)0
print('uuid: ', decoded_info)