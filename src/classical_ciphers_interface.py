from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from classical_ciphers import (
    encrypt_caesar,
    decrypt_caesar,
    encrypt_vigenere,
    decrypt_vigenere,
    encrypt_beaufort,
    encrypt_affine,
    decrypt_affine,
)
from math import gcd
from index_of_coincidence import index_of_coincidence
from helper_functions import print_result


def validate_number_between_1_and_26(num: str) -> bool:
    if num.strip().isnumeric():
        if int(num) >= 1 and int(num) <= 26:
            return True
    return False


def validate_number_coprime_with_26(num: str) -> bool:
    if num.strip().isnumeric():
        if gcd(int(num), 26) == 1:
            return True
    return False


class CaesarInterface:
    EXIT_ACTION = "Exit caesar cipher"
    NEW_MESSAGE_ACTION = "Encrypt/decrypt new message"
    CHANGE_KEY_ACTION = "Change key"

    def run(self):
        self.ask_key()
        self.encrypt_or_decrypt_message()
        while True:
            action = self.ask_action()
            if action == self.EXIT_ACTION:
                break
            elif action == self.NEW_MESSAGE_ACTION:
                self.encrypt_or_decrypt_message()
            elif action == self.CHANGE_KEY_ACTION:
                self.ask_key()

    def ask_key(self):
        shift_value = inquirer.text(
            message="Enter key (shift) value:",
            validate=validate_number_between_1_and_26,
            invalid_message="Shift must be an integer between 1 and 26",
        ).execute()
        self.shift_value = int(shift_value)

    def encrypt_or_decrypt_message(self):
        message = inquirer.text(message="Enter message to encrypt/decrypt:", multiline=True).execute()
        encrypt_mode = inquirer.select(
            message="Select action:",
            choices=(Choice(True, name="Encrypt message"), Choice(False, name="Decrypt message")),
        ).execute()
        if encrypt_mode:
            result = encrypt_caesar(message, self.shift_value)
        else:
            result = decrypt_caesar(message, self.shift_value)
        print_result(result)

    def ask_action(self) -> str:
        action_to_perform = inquirer.select(
            message="Select next action:", choices=(self.NEW_MESSAGE_ACTION, self.CHANGE_KEY_ACTION, self.EXIT_ACTION)
        ).execute()
        return action_to_perform


class VigenereInterface(CaesarInterface):
    EXIT_ACTION = "Exit Vigenere cipher"
    NEW_MESSAGE_ACTION = "Encrypt/decrypt new message"
    CHANGE_KEY_ACTION = "Change key"

    def ask_key(self):
        key = inquirer.text(
            message="Enter key:",
            validate=lambda x: x.strip().isalpha(),
            invalid_message="Key must a sequence of letters",
        ).execute()
        self.key = key.strip()

    def encrypt_or_decrypt_message(self):
        message = inquirer.text(message="Enter message to encrypt/decrypt:", multiline=True).execute()
        encrypt_mode = inquirer.select(
            message="Select action:",
            choices=(Choice(True, name="Encrypt message"), Choice(False, name="Decrypt message")),
        ).execute()
        if encrypt_mode:
            result = encrypt_vigenere(message, self.key)
        else:
            result = decrypt_vigenere(message, self.key)
        print_result(result)


class BeaufortInterface(VigenereInterface):
    EXIT_ACTION = "Exit Beaufort cipher"

    def encrypt_or_decrypt_message(self):
        message = inquirer.text(message="Enter message to encrypt/decrypt:", multiline=True).execute()
        result = encrypt_beaufort(message, self.key)
        print_result(result)


class AffineInterface(CaesarInterface):
    EXIT_ACTION = "Exit affine cipher"
    NEW_MESSAGE_ACTION = "Encrypt/decrypt new message"
    CHANGE_KEY_ACTION = "Change coefficients"

    def ask_key(self):
        a = inquirer.text(
            message="Enter 'a' coefficient:",
            instruction="(for ax + b)",
            validate=validate_number_coprime_with_26,
            invalid_message="a coefficient must be an integer coprime with 26",
        ).execute()
        self.a = int(a)

        b = inquirer.text(
            message="Enter 'b' coefficient:",
            instruction="(for ax + b)",
            validate=validate_number_between_1_and_26,
            invalid_message="b coefficient must be an integer between 1 and 26",
        ).execute()
        self.b = int(b)

    def encrypt_or_decrypt_message(self):
        message = inquirer.text(message="Enter message to encrypt/decrypt:", multiline=True).execute()
        encrypt_mode = inquirer.select(
            message="Select action:",
            choices=(Choice(True, name="Encrypt message"), Choice(False, name="Decrypt message")),
        ).execute()
        if encrypt_mode:
            result = encrypt_affine(message, self.a, self.b)
        else:
            result = decrypt_affine(message, self.a, self.b)
        print_result(result)


class IndexOfCoincidenceInterface:
    EXIT_ACTION = "Exit index of coincidence calculator"
    NEW_TEXT_ACTION = "Enter a new text"

    def run(self):
        while True:
            self.ask_text()
            action = self.ask_action()
            if action == self.EXIT_ACTION:
                break

    def ask_text(self):
        text = inquirer.text(message="Enter text to analyse:", multiline=True, mandatory=False).execute()
        try:
            IoC_calculated = round(index_of_coincidence(text), 5)
            print_result(str(IoC_calculated))
        except ZeroDivisionError:
            color_print((["red", "Index of coincidence is not defined"],))

    def ask_action(self):
        action_to_perform = inquirer.select(
            message="Select next action:", choices=(self.NEW_TEXT_ACTION, self.EXIT_ACTION)
        ).execute()
        return action_to_perform


if __name__ == "__main__":
    CaesarInterface().run()
    VigenereInterface().run()
    AffineInterface().run()
