import fileinput

for encoded in fileinput.input(files='8.txt'):
    encoded = encoded.strip()
    cipherBlocks = set()
    iterations = len(encoded) // 16
    usedECB = False
    for i in range(iterations):
        block = encoded[16 * i:16 * i + 16]
        if block in cipherBlocks:
            usedECB = True
        else:
            cipherBlocks.add(block)
    if usedECB:
        print(encoded)
