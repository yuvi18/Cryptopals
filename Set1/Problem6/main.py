import fileinput
import base64
import statistics


# Hamming Distance
def hammingDistance(string1, string2):
    byteString1 = string1
    byteString2 = string2
    hamDistance = 0
    for byte in range(0, len(byteString1)):
        xorString = bin((byteString1[byte] ^ byteString2[byte]))
        for value in range(0, len(xorString)):
            if xorString[value] == '1':
                hamDistance += 1
    return hamDistance


# Frequency Code
def get_english_score(input_bytes):
    """Compares each input byte to a character frequency
    chart and returns the score of a message based on the
    relative frequency the characters occur in the English
    language
    """

    # From https://en.wikipedia.org/wiki/Letter_frequency
    # with the exception of ' ', which I estimated.
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])


# Challenge Code

base64Encoded = ""

for encoded in fileinput.input(files='6.txt'):
    encoded = encoded.strip()
    base64Encoded += encoded

encodedBytes = base64.b64decode(base64Encoded)

#encodedBytes = bytearray.fromhex("3c0804390c0b1415571d321307083807080b0332081a1938000b381602124e10")

minimumEditDistance = 500
testKEYSIZE = 0
keysize_distances = {}
most_likely_keysize = 3
for keysize in range(3, 41):
    distances = []

    for iteration in range(50):
        try:
            start1 = 0 + (iteration * keysize)
            end1 = start1 + keysize
            start2 = end1
            end2 = start2 + keysize
            distance = hammingDistance(encodedBytes[start1:end1], encodedBytes[start2:end2])
            distances.append(distance / keysize)
        except IndexError:
            continue
    avg_distance = statistics.mean(distances)
    keysize_distances[keysize] = avg_distance
    most_likely_keysize = sorted(keysize_distances.items(), key=lambda x: x[1])[0][0]

testKEYSIZE = most_likely_keysize
cipherBlocks = []
iterations = len(encodedBytes) // testKEYSIZE
leftover = len(encodedBytes) % testKEYSIZE

for characters in range(testKEYSIZE):
    cipherBlocks.append(bytearray(b""))
    for i in range(iterations):
        cipherBlocks[characters].append(encodedBytes[i * testKEYSIZE + characters])

remainingBytes = encodedBytes[-leftover:]

for i in range(len(remainingBytes)):
    cipherBlocks[i].append(remainingBytes[i])

# Solve Each Single Character XOR

finalKey = bytearray(b"")

for j in range(testKEYSIZE):
    maxScore = 0
    keyValue = 0
    for i in range(0, 128):
        finalValue = b""
        for testValue in range(0, len(cipherBlocks[j])):
            finalValue += (cipherBlocks[j][testValue] ^ i).to_bytes(1, "big")
        score = get_english_score(finalValue)
        if maxScore <= score:
            maxScore = score
            keyValue = i

    finalKey.append(keyValue)


# Verify Answer

def repeatingXOR(text, key):
    encryptIndex = 0
    finalAnswer = b""
    for byte in range(0, len(text)):
        finalAnswer += (text[byte] ^ key[encryptIndex]).to_bytes(1, "big")
        encryptIndex += 1
        if encryptIndex == len(key):
            encryptIndex = 0
    return finalAnswer


print(repeatingXOR(encodedBytes, finalKey).decode("utf-8"))
