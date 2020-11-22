import qrcode

data =  {'nombre' : 'Santiago', 'edad' : 21, 'CC': 1144107262}
img = qrcode.make(data)
filename = "QR_Code.png"
#f = open("QR_Code.png", "wb")
#img.save(f)
#f.close()
img.save(filename)
