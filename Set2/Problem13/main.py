import os

from Crypto.Cipher import AES


def addpadding(byteString, length):
    currentAmount = len(byteString)
    padding = byteString
    if currentAmount % length != 0:
        padding = b"" + byteString + \
                  (length - (currentAmount % length)) * (length - (currentAmount % length)).to_bytes(1, "little")
    return padding


def removepadding(byteString):
    paddingAmt = int(byteString[-1])
    return byteString[:-paddingAmt]


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


def kVParse(orig):
    interim = orig.split("&")
    output = {}
    for i in interim:
        kV = i.split("=")
        output[kV[0]] = kV[1]
    return output


def profile_for(email):
    email = email.replace("&", "")
    email = email.replace("=", "")
    return "email=" + email + "&uid=10&role=user"


def findBlocksize(oracle):
    i = 1
    prevLength = -1
    blockSize = -1
    second = False
    while True:
        test = "A" * i
        newLength = len(oracle(test.encode('utf-8')))
        if prevLength != newLength and prevLength != -1:
            if second:
                blockSize = i - blockSize
                break
            blockSize = i
            second = True
        prevLength = newLength
        i += 1

    return blockSize


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


randomKey = os.urandom(16)


def ecbOracle(userEmail):
    cipher = AES.new(randomKey, AES.MODE_ECB)
    finalPlaintext = profile_for(userEmail).encode()
    finalPlaintext = addpadding(finalPlaintext, 16)
    finalCiphertext = bytearray(cipher.encrypt(finalPlaintext))
    return finalCiphertext


def decryptProfile(encrypted):
    cipher = AES.new(randomKey, AES.MODE_ECB)
    profilePlaintext = bytearray(cipher.decrypt(encrypted))
    noPadding = removepadding(profilePlaintext)
    return kVParse(noPadding.decode())


testEmail = "whoami@yahoo.com"

testEncrypted = ecbOracle(testEmail)
print(testEncrypted)
testProfile = decryptProfile(testEncrypted)
print(testProfile)
