phrase = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
encryptKey = b"ICE"


def repeatingXOR(text, key):
    encryptIndex = 0
    finalValue = b""
    for byte in range(0, len(text)):
        finalValue += (text[byte] ^ key[encryptIndex]).to_bytes(1, "big")
        encryptIndex += 1
        if encryptIndex == len(key):
            encryptIndex = 0
    return finalValue


answer = repeatingXOR(phrase, encryptKey).hex()

assert answer == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276" \
                 "5272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

print(answer)
