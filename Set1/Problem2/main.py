byteString1 = bytes.fromhex("1c0111001f010100061a024b53535009181c")
byteString2 = bytes.fromhex("686974207468652062756c6c277320657965")

finalValue = b""

for byte in range(0, len(byteString1)):
    finalValue += (byteString1[byte] ^ byteString2[byte]).to_bytes(1, "big")

assert finalValue.hex() == "746865206b696420646f6e277420706c6179"

print(finalValue.hex())
