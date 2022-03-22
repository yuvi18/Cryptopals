def addpadding(byteString, length):
    currentAmount = len(byteString)
    padding = byteString
    if currentAmount % length != 0:
        padding = b"" + byteString + (length - currentAmount % length) * b"\x04"
    return padding


result = addpadding(b"YELLOW SUBMARINE", 7)
print(result)
