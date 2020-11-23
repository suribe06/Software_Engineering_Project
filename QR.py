import qrcode

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
    img.save('QR_Code.png')
