import base64
from Crypto.Cipher import AES

file = open("7.txt", "r")
encoded = file.read()

theBytes = base64.b64decode(encoded)

cipher = AES.new(b"YELLOW SUBMARINE", AES.MODE_ECB)

answer = cipher.decrypt(theBytes)

print(answer.decode('utf-8'))
