import qrcode
import uuid


def generate_box():
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
    img.save("box1.png")
    return box_id


print(generate_box())
