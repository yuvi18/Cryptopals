import base64

byteString = bytes.fromhex("49276d206b696c6c696e6720796f757220627261696e20"
                           "6c696b65206120706f69736f6e6f7573206d757368726f6f6d")

result = base64.b64encode(byteString)

stringResult = result.decode("utf-8")

assert stringResult == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

print(stringResult)
