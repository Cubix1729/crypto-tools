from helper_functions import *
from math import gcd


def encrypt_caesar(text: str, shift: int, preserve_non_alphabetic_characters=False):
    """Encrypts text with the Caesar cipher, using the shift/key given"""
    if not preserve_non_alphabetic_characters:
        text = to_upper_case_without_punctuation_or_spaces(text)

    ciphertext_letters = []
    for letter in text:
        if not letter.isalpha():
            ciphertext_letters.append(letter)
            continue
        letter = letter.upper()
        ciphertext_letters.append(shift_letter(letter=letter, offset=shift))

    return "".join(ciphertext_letters)


def decrypt_caesar(text: str, shift: int, preserve_non_alphabetic_characters=False):
    """Decrypts text with the Caesar cipher, using the shift/key given"""
    return encrypt_caesar(
        text=text, shift=-shift, preserve_non_alphabetic_characters=preserve_non_alphabetic_characters
    )


def encrypt_vigenere(text: str, key: str, preserve_non_alphabetic_characters=False):
    """Encrypts text with the Vigenere cipher, using the key given"""
    if not preserve_non_alphabetic_characters:
        text = to_upper_case_without_punctuation_or_spaces(text)
    key = key.upper()

    ciphertext_letters = []
    key_length = len(key)
    index = 0
    for letter in text:
        if not letter.isalpha():
            ciphertext_letters.append(letter)
            continue
        letter = letter.upper()
        corresponding_key_letter = key[index % key_length]
        encrypted_letter = shift_letter(letter, letter_index(corresponding_key_letter) - 1)
        ciphertext_letters.append(encrypted_letter)

        index += 1

    return "".join(ciphertext_letters)


def decrypt_vigenere(text: str, key: str, preserve_non_alphabetic_characters=False):
    """Decrypts text with the Vigenere cipher, using the key given"""
    if not preserve_non_alphabetic_characters:
        text = to_upper_case_without_punctuation_or_spaces(text)
    key = key.upper()

    ciphertext_letters = []
    key_length = len(key)
    index = 0
    for letter in text:
        if not letter.isalpha():
            ciphertext_letters.append(letter)
            continue
        letter = letter.upper()
        corresponding_key_letter = key[index % key_length]
        encrypted_letter = shift_letter(letter, -letter_index(corresponding_key_letter) + 1)
        ciphertext_letters.append(encrypted_letter)

        index += 1

    return "".join(ciphertext_letters)


def encrypt_beaufort(text: str, key: str, preserve_non_alphabetic_characters=False):
    """Encrypts text with the Beaufort cipher, using the key given"""
    if not preserve_non_alphabetic_characters:
        text = to_upper_case_without_punctuation_or_spaces(text)
    key = key.upper()

    ciphertext_letters = []
    key_length = len(key)
    index = 0
    for letter in text:
        if not letter.isalpha():
            ciphertext_letters.append(letter)
            continue
        letter = letter.upper()
        corresponding_key_letter = key[index % key_length]
        text_letter_index = letter_index(letter)
        encrypted_letter = shift_letter(corresponding_key_letter, -text_letter_index + 1)
        ciphertext_letters.append(encrypted_letter)

        index += 1

    return "".join(ciphertext_letters)


def decrypt_beaufort(text: str, key: str, preserve_non_alphabetic_characters=False):
    """Decrypts text with the Beaufort cipher, using the key given"""
    return encrypt_beaufort(text, key, preserve_non_alphabetic_characters)


def generate_affine_subsitution(a: int, b: int) -> dict:
    """Generate the affine substitution defined by ax + b as a dictionary"""
    if gcd(a, 26) != 1:
        raise ValueError("Invalid value for a: a must be prime with 26")
    mapping = {}
    for letter in string.ascii_uppercase:
        original_index = letter_index(letter) - 1  # Transforming 1-based indexing to 0-based indexing
        transformed_index = (a * original_index + b) % 26
        transformed_letter = letter_from_index(transformed_index + 1)  # Transforming 0-based to 1-based indexing
        mapping[letter] = transformed_letter

    return mapping


def encrypt_affine(text: str, a: int, b: int, preserve_non_alphabetic_characters=False) -> str:
    if not preserve_non_alphabetic_characters:
        text = to_upper_case_without_punctuation_or_spaces(text)
    substitution = generate_affine_subsitution(a, b)
    ciphertext_letters = []
    for letter in text:
        if not letter.isalpha():
            ciphertext_letters.append(letter)
            continue

        letter = letter.upper()
        encrypted_letter = substitution[letter]
        ciphertext_letters.append(encrypted_letter)

    return "".join(ciphertext_letters)


def decrypt_affine(text: str, a: int, b: int, preserve_non_alphabetic_characters=False) -> str:
    if not preserve_non_alphabetic_characters:
        text = to_upper_case_without_punctuation_or_spaces(text)
    substitution = {v: k for k, v in generate_affine_subsitution(a, b).items()}
    ciphertext_letters = []
    for letter in text:
        if not letter.isalpha():
            ciphertext_letters.append(letter)
            continue

        letter = letter.upper()
        encrypted_letter = substitution[letter]
        ciphertext_letters.append(encrypted_letter)

    return "".join(ciphertext_letters)
