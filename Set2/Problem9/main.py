def addpadding(byteString, length):
    currentAmount = len(byteString)
    padding = byteString
    if currentAmount % length != 0:
        padding = b"" + byteString +\
                  (length - (currentAmount % length)) * (length - (currentAmount % length)).to_bytes(1, "little")
    return padding


result = addpadding(b"YELLOW SUBMARINE", 7)
print(result)
