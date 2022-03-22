import base64
import fileinput
from Crypto.Cipher import AES

for encoded in fileinput.input(files='7.txt'):
    byteEncoded += encoded

byteEncoded = base64.b64decode(byteEncoded)
key = b"YELLOW SUBMARINE"

cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(byteEncoded)

print(plaintext.decode('utf-8'))
