import base64

def encriptar(password):
    encoded = None
    if password != None:
        password_encrypt = password.encode()
        encoded = base64.b64encode(password_encrypt)
        encoded = encoded.decode()
    return encoded

def decriptar(encoded):
    p = encoded.encode()
    decoded = base64.b64decode(p)
    password_decrypt = decoded.decode('utf-8')
    return password_decrypt
