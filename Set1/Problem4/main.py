import fileinput


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


# Challenge Code Starts

encoded = b""
maxScore = 0
answer = b""

for encoded in fileinput.input(files='4.txt'):
    encoded = encoded.strip()
    encoded = bytes.fromhex(encoded)
    for i in range(0, 128):
        finalValue = b""
        for testValue in range(0, len(encoded)):
            finalValue += (encoded[testValue] ^ i).to_bytes(1, "big")
        score = get_english_score(finalValue)
        if maxScore <= score:
            maxScore = score
            answer = finalValue

print(answer.decode("utf-8"))
