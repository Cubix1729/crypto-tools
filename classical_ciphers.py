from helper_functions import *


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
