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


def kVParse(orig):
    interim = orig.split("&")
    output = {}
    for i in interim:
        kV = i.split("=")
        output[kV[0]] = kV[1]
    return output


def profile_for(email):
    email = email.replace(b"&", b"")
    email = email.replace(b"=", b"")
    return b"email=" + email + b"&uid=10&role=user"


randomKey = os.urandom(16)
blockSize = 16


def ecbOracle(userEmail):
    cipher = AES.new(randomKey, AES.MODE_ECB)
    finalPlaintext = profile_for(userEmail)
    finalPlaintext = addpadding(finalPlaintext, blockSize)
    finalCiphertext = bytearray(cipher.encrypt(finalPlaintext))
    return finalCiphertext


def decryptProfile(encrypted):
    cipher = AES.new(randomKey, AES.MODE_ECB)
    profilePlaintext = bytearray(cipher.decrypt(encrypted))
    noPadding = removepadding(profilePlaintext)
    return kVParse(noPadding.decode())


# Can't set email to the admin profile string and use ECB's property since our profile encoder removes encoding strings.
# Step 1: Figure out how to write admin + padding in cipher text
# Step 2: Get everything up until role= as cipher text with some arbitrary email aligned on 16 byte padding.
# Step 3: Add step1's cipher text to the end of step2's cipher text.
# Step 4: Decrypt profile (and profit!)

# Step 1
emailPrefix = b"email="
emailPadding = b"A" * (blockSize - len(emailPrefix))
emailAdmin = addpadding(b"admin", blockSize)
adminEncryptedBlock = ecbOracle(emailPadding + emailAdmin)[blockSize: 2 * blockSize]
