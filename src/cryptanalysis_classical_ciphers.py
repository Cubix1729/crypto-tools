from cryptanalysis_frequencies import LETTER_FRENQUENCIES, MOST_COMMON_BIGRAMS, MOST_COMMON_TRIGRAMS
from classical_ciphers import (
    encrypt_caesar,
    decrypt_caesar,
    encrypt_affine,
    decrypt_affine,
    encrypt_vigenere,
    decrypt_vigenere,
)
from index_of_coincidence import *
from helper_functions import *
from random import randrange
import copy


def frequencies_score(text: str) -> float:
    """Returns a score measuring how 'English' letter frequencies are in a text"""
    text = to_upper_case_without_punctuation_or_spaces(text)
    score = 0
    for letter in text:
        score += LETTER_FRENQUENCIES[letter]
    return score / len(text)


def bigram_score(text: str) -> float:
    """Returns a score measuring how 'English' bigram frequencies are in a text"""
    text = to_upper_case_without_punctuation_or_spaces(text)
    score = 0
    for index in range(len(text) - 1):
        bigram = text[index] + text[index + 1]
        score += MOST_COMMON_BIGRAMS.get(bigram, 0)
    return score / len(text)


def trigram_score(text: str) -> float:
    """Returns a score measuring how 'English' trigram frequencies are in a text"""
    text = to_upper_case_without_punctuation_or_spaces(text)
    score = 0
    for index in range(len(text) - 2):
        trigram = text[index] + text[index + 1] + text[index + 2]
        score += MOST_COMMON_TRIGRAMS.get(trigram, 0)
        return score / len(text)


def english_score(text: str) -> float:
    """Returns a score meant to measure how 'English' is a text'"""
    return frequencies_score(text) / 3 + bigram_score(text) * 3 + trigram_score(text) * 50


def break_caesar(text: str) -> tuple:
    """Takes a ciphertext encrypted with the Caesar cipher and returns the most probable key"""
    best_text = ""
    best_key = 0
    best_score = 0
    for key in range(1, 26):
        decrypted_text = decrypt_caesar(text, key)
        corresponding_score = english_score(decrypted_text)
        if corresponding_score > best_score:
            best_score = corresponding_score
            best_text = decrypted_text
            best_key = key
    return best_key


def break_affine(text: str) -> tuple:
    """Takes a ciphertext encrypted with the affine cipher and returns (the most probable a coefficient, the corresponding b coefficient)"""
    best_text = ""
    best_a = 0
    best_b = 0
    best_score = 0
    for a in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        for b in range(0, 26):
            decrypted_text = decrypt_affine(text, a, b)
            corresponding_score = english_score(decrypted_text)
            if corresponding_score > best_score:
                best_score = corresponding_score
                best_text = decrypted_text
                best_a = a
                best_b = b
    return (best_a, best_b)


def key_length(text: str, min_len: int = 2, max_len: int = 8) -> int:
    """Takes a ciphertext encrypted with the Vigenere cipher and returns the most probable key length used within the interval specified"""
    text = to_upper_case_without_punctuation_or_spaces(text)
    best_key_length = 0
    best_IoC = 0
    for length in range(min_len, max_len + 1):
        slices = [""] * length
        for index in range(len(text)):
            letter = text[index]
            slices[index % length] += letter

        slices_IoC = []
        for single_slice in slices:
            if len(single_slice) > 1:
                slices_IoC.append(index_of_coincidence(single_slice))
        IoC_mean = sum(slices_IoC) / length

        if IoC_mean > best_IoC:
            best_IoC = IoC_mean
            best_key_length = length
    return best_key_length


def find_offset(text: str) -> int:
    """Helper function for decrypting Vigenere cipher"""
    best_text = ""
    best_key = 0
    best_score = 0
    for key in range(1, 26):
        decrypted_text = decrypt_caesar(text, key)
        corresponding_score = frequencies_score(decrypted_text)
        if corresponding_score > best_score:
            best_score = corresponding_score
            best_text = decrypted_text
            best_key = key
    return best_key


def break_vigenere(text: str, key_length: int):
    text = to_upper_case_without_punctuation_or_spaces(text)
    key = ""
    for key_letter_index in range(key_length):
        corresponding_slice = []
        for index in range(key_letter_index, len(text), key_length):
            corresponding_slice.append(text[index])
        print(find_offset("".join(corresponding_slice)))
        key_letter_found = letter_from_index(find_offset("".join(corresponding_slice)) + 1)
        key += key_letter_found
    return key
