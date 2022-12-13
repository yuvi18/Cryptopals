import base64
import os

from Crypto.Cipher import AES


def addpadding(byteString, length):
    currentAmount = len(byteString)
    padding = byteString
    if currentAmount % length != 0:
        padding = b"" + byteString + (length - currentAmount % length) * b"\x04"
    return padding


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

    return usedECB


randomKey = os.urandom(16)

unknown = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lyb" \
          "GllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK "


def ecbOracle(regularByteString):
    cipher = AES.new(randomKey, AES.MODE_ECB)

    finalPlaintext = regularByteString + base64.b64decode(unknown)
    finalPlaintext = addpadding(finalPlaintext, 16)

    finalCiphertext = bytearray(cipher.encrypt(finalPlaintext))

    return finalCiphertext


# Oracle that I know for debugging
def ecbOracle2(regularByteString):
    cipher = AES.new(randomKey, AES.MODE_ECB)

    finalPlaintext = regularByteString + b"Hey there! This is the text I am trying to obtain."
    finalPlaintext = addpadding(finalPlaintext, 16)

    finalCiphertext = bytearray(cipher.encrypt(finalPlaintext))

    return finalCiphertext


def findBlocksize():
    i = 1
    prevLength = -1
    blockSize = -1
    second = False
    while True:
        test = "A" * i
        newLength = len(ecbOracle(test.encode('utf-8')))
        if prevLength != newLength and prevLength != -1:
            if second:
                blockSize = i - blockSize
                break
            blockSize = i
            second = True
        prevLength = newLength
        i += 1

    return blockSize


# Discover Blocksize
theBlocksize = findBlocksize()

# Detect ECB
testString = "A" * theBlocksize * 2

if detect_ecb(bytes(ecbOracle(testString.encode('utf-8')))):
    print("Oracle uses ECB! Let's go!")
else:
    print("Uh oh, Oracle doesn't use ECB!")


# Crack ECB

def decode_ecb(blocksize, theOracle):
    answer = b""
    blocks = len(theOracle(b"")) // blocksize
    for blockNum in range(0, blocks):
        block = b""
        for byteIndex in range(1, blocksize + 1):
            if blockNum == 0:
                baseBytes = b"A" * (blocksize - byteIndex)
            else:
                baseBytes = answer[(blockNum - 1) * 16: blockNum * 16][byteIndex:16]
            dummyBytes = baseBytes
            target = theOracle(dummyBytes)[blockNum * 16: (blockNum + 1) * 16]
            for i in range(0, 256):
                newBytes = baseBytes + block + i.to_bytes(1, "big")
                encoded = theOracle(newBytes)[0:16]
                if target == encoded:
                    block = block + i.to_bytes(1, "big")
                    break

        answer += block

    return answer


decodedBytes = decode_ecb(theBlocksize, ecbOracle)

print(decodedBytes.decode('utf-8'))
