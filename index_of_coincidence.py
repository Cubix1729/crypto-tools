from enigma_machine import to_upper_case_without_punctuation_or_spaces
import string


def index_of_coincidence(text: str) -> int:
    text = to_upper_case_without_punctuation_or_spaces(text)
    numerator = 0
    for letter in string.ascii_uppercase:
        letter_count_in_text = text.count(letter)
        numerator += letter_count_in_text * (letter_count_in_text - 1)
    denominator = len(text) * (len(text) - 1)
    return numerator / denominator
