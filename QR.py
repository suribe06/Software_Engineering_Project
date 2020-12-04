import qrcode
from PIL import Image
import cv2
from pyzbar import pyzbar

def makeQR(data):
    #Se crea el QR
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=3)
    #Se agrega la informacion al qr
    for key, value in data.items():
        qr.add_data("{0} : {1}\n".format(key,value))
    qr.make(fit=True)
    #Se guarda el qr como imagen
    img = qr.make_image(fill='black', back_color='white')
    img.save('static/images/QR_{0}.png'.format(data["Numero Documento"]))

def readQR(filename):
    #Se abre el codigo QR
    img = Image.open('static/images/uploads/{0}'.format(filename))
    #Se decodifica el qr
    output = pyzbar.decode(img)
    output_decode = output[0].data.decode()
    #Se parsea la informacion
    x = output_decode.split('\n')
    x.pop()
    data = []
    for d in x:
        data.append((d.split(':')[1]).strip())
    return data
