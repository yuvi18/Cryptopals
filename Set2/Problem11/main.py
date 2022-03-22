import os
import random

from Crypto.Cipher import AES


def addpadding(byteString, length):
    currentAmount = len(byteString)
    padding = byteString
    if currentAmount % length != 0:
        padding = b"" + byteString + (length - currentAmount % length) * b"\x04"
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
    for j in range(blocks):
        decryptedBlock = ecbCipher.decrypt(encodedBytes[j * 16: (j + 1) * 16])
        if j == 0:
            decryptedBlock = xorByteStrings(IV, decryptedBlock)
        else:
            decryptedBlock = xorByteStrings(encodedBytes[(j - 1) * 16: j * 16], decryptedBlock)
        newPlainText.extend(decryptedBlock)
    return newPlainText


def detect_ecb(detectionText):
    cipherBlocks = set()
    iterations = len(detectionText) // 16
    usedECB = False
    for k in range(iterations):
        block = detectionText[16 * k:16 * k + 16]
        if block in cipherBlocks:
            usedECB = True
        else:
            cipherBlocks.add(block)
    if usedECB:
        print("ECB")
    else:
        print("CBC")


def encryption_oracle(regularByteString):
    randomKey = os.urandom(16)
    cipher = AES.new(randomKey, AES.MODE_ECB)
    beginRandomBytes = os.urandom(random.randint(5, 10))
    endRandomBytes = os.urandom(random.randint(5, 10))
    finalPlaintext = beginRandomBytes + regularByteString + endRandomBytes
    finalPlaintext = addpadding(finalPlaintext, 16)
    if random.randint(1, 2) == 1:
        finalCiphertext = bytearray(cipher.encrypt(finalPlaintext))
    else:
        randIV = os.urandom(16)
        finalCiphertext = encryptCBC(cipher, finalPlaintext, randIV)

    detect_ecb(bytes(finalCiphertext))

    return finalCiphertext


for iteration in range(50):
    encryption_oracle(b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
