import qrcode
import uuid


def generate_QR():
    box_id = uuid.uuid1()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(box_id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return box_id, img


def generate_boxes(n):
    f = open("qr_codes.txt", "w")

    for i in range(n):
        box_id, img = generate_QR()
        f.write(str(i) + "," + str(box_id) + "\n")
        img.save(str(i) + ".png")

    f.close()

generate_boxes(15)
