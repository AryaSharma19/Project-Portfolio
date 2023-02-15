"""A ceasar cipher encoder and decoder set to an offset of one. Works for Uppercase and Lowercase and any length and any offset."""
__author__ = "Arya"


numbers_in_the_alphabet: int = 26
lc_ascii_code_normalizer: int = 97
uppercase_ascii_code_normalizer: int = 65
first_letter: int = 0

def encode_char(x: str) -> str:
    """Returns an encoded letter adjusted to case."""
    if ((64 >= ord(x)) or ( 91 <= ord(x) and ord(x) <= 96) or (123 <= ord(x))):
        return x
    else: 
        if x.isupper():
            character: str = x
            ascii_code: int = ord(character)
            normalized_code: int = ascii_code - uppercase_ascii_code_normalizer
            encoded_code: int = (normalized_code + offset) % numbers_in_the_alphabet + uppercase_ascii_code_normalizer
            encoded_character: str = chr(encoded_code)
            return encoded_character
        else:
            lowercase_character: str = x
            lowercase_ascii_code: int = ord(lowercase_character)
            lc_normalized_code: int = lowercase_ascii_code - lc_ascii_code_normalizer
            lc_encoded_code: int = (lc_normalized_code + offset) % numbers_in_the_alphabet + lc_ascii_code_normalizer
            lowercase_encoded_character: str = chr(lc_encoded_code)
            return lowercase_encoded_character

def encode(x: str) -> str:
    """Returns an encoded word of any length."""
    word: str = ""
    i: int = 0
    while i < (len(x)):
        letter: str = encode_char(x[i])
        word = word + letter
        i = i + 1
    return word

def decode_char(x: str) -> str:
    """Returns a decoded letter adjusted to case."""
    if ((64 >= ord(x)) or ( 91 <= ord(x) and ord(x) <= 96) or (123 <= ord(x))):
        return x
    else:
        if x.isupper():
            character: str = x
            ascii_code: int = ord(character)
            normalized_code: int = ascii_code - uppercase_ascii_code_normalizer
            decoded_code: int = (normalized_code - offset) % numbers_in_the_alphabet + uppercase_ascii_code_normalizer
            decoded_character: str = chr(decoded_code)
            return decoded_character
        else:
            lowercase_character: str = x
            lowercase_ascii_code: int = ord(lowercase_character)
            lc_normalized_code: int = lowercase_ascii_code - lc_ascii_code_normalizer
            lc_decoded_code: int = (lc_normalized_code - offset) % numbers_in_the_alphabet + lc_ascii_code_normalizer
            lowercase_decoded_character: str = chr(lc_decoded_code)
            return lowercase_decoded_character

def decode(x: str) -> str:
    """Returns an decoded word of any length."""
    word: str = ""
    i: int = 0
    while i < (len(x)):
        letter: str = decode_char(x[i])
        word = word + letter
        i = i + 1
    return word

offset: int = int(input("Offset:"))
print(encode(str(input("Plaintext: "))))
print(decode(str(input("Ciphertext: "))))