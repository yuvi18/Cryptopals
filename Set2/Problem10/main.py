import fileinput
import base64
from Crypto.Cipher import AES


def addpadding(byteString, length):
    currentAmount = len(byteString)
    padding = byteString
    if currentAmount % length != 0:
        padding = b"" + byteString +\
                  (length - (currentAmount % length)) * (length - (currentAmount % length)).to_bytes(1, "little")
    return padding


def xorByteStrings(byteString1, byteString2):
    finalValue = b""

    for byte in range(0, len(byteString1)):
        finalValue += (byteString1[byte] ^ byteString2[byte]).to_bytes(1, "big")

    return finalValue


def encryptCBC(ecbCipher, plaintextBytes, IV):
    blocks = len(plaintextBytes) // 16
    newCipherText = bytearray()
    for i in range(blocks):
        if i == 0:
            xorString = xorByteStrings(IV, plaintextBytes[i * 16: (i + 1) * 16])
        else:
            xorString = xorByteStrings(newCipherText[(i - 1) * 16: i * 16], plaintextBytes[i * 16: (i + 1) * 16])
        encryptedBlock = ecbCipher.encrypt(xorString)
        newCipherText.extend(encryptedBlock)
    return newCipherText


def decryptCBC(ecbCipher, encodedBytes, IV):
    blocks = len(encodedBytes) // 16
    newPlainText = bytearray()
    for i in range(blocks):
        decryptedBlock = ecbCipher.decrypt(encodedBytes[i * 16: (i + 1) * 16])
        if i == 0:
            decryptedBlock = xorByteStrings(IV, decryptedBlock)
        else:
            decryptedBlock = xorByteStrings(encodedBytes[(i - 1) * 16: i * 16], decryptedBlock)
        newPlainText.extend(decryptedBlock)
    return newPlainText


# Driver Code

bytesEncoded = ""

for encoded in fileinput.input(files='10.txt'):
    bytesEncoded += encoded

bytesEncoded = base64.b64decode(bytesEncoded)

key = b"YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)
codeIV = b"\x00" * 16

result = decryptCBC(cipher, bytesEncoded, codeIV)

print(result.decode("utf-8"))
