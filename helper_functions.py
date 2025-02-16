import string
import re


def to_number_between_1_and_26(letter_index: int) -> int:
    """Converts a letter index to a number between 1 and 26"""
    return ((letter_index - 1) % 26) + 1


def to_upper_case_without_punctuation_or_spaces(text: str) -> str:
    """Changes all the letters to upper case, and removes any character that isn't a letter"""
    return re.sub("[^A-Z]", "", text.upper())


def letter_index(letter: str) -> int:
    """Returns the index in the alphabet of the letter given (with A=1)"""
    return string.ascii_uppercase.index(letter.upper()) + 1


def letter_from_index(index: int) -> str:
    """From a letter index given, it returns the corresponding uppercase letter (A=1)"""
    return string.ascii_uppercase[index - 1]


def shift_letter(letter: str, offset: int) -> str:
    """Shifts by offset the given letter in the alphabet"""
    return letter_from_index(to_number_between_1_and_26(letter_index(letter) + offset))


def rotate_rotor(rotor: str, offset: int = 1) -> str:
    """Rotates (shifts) a given rotor by the given offset"""
    return rotor[offset:] + rotor[0:offset]
