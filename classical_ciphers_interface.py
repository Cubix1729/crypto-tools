from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from classical_ciphers import encrypt_caesar, decrypt_caesar, encrypt_vigenere, decrypt_vigenere


def validate_number_between_1_and_26(num: str) -> bool:
    if num.strip().isnumeric():
        if int(num) >= 1 and int(num) <= 26:
            return True
    return False


class CaesarInterface:
    EXIT_ACTION = "Exit caesar cipher"
    NEW_MESSAGE_ACTION = "Encrypt/decrypt new message"
    CHANGE_KEY_ACTION = "Change key"
    def run(self):
        self.ask_shift_value()
        self.encrypt_or_decrypt_message()
        while True:
            action = self.ask_action()
            if action == self.EXIT_ACTION:
                break
            elif action == self.NEW_MESSAGE_ACTION:
                self.encrypt_or_decrypt_message()
            elif action == self.CHANGE_KEY_ACTION:
                self.ask_shift_value()
    
    def ask_shift_value(self):
        shift_value = inquirer.text(
            message="Enter key (shift) value:",
            validate=validate_number_between_1_and_26,
            invalid_message="Shift must be an integer between 1 and 26"
        ).execute()
        self.shift_value = int(shift_value)
    
    def encrypt_or_decrypt_message(self):
        message = inquirer.text(
            message="Enter message to encrypt/decrypt:",
            multiline=True
        ).execute()
        encrypt_mode = inquirer.select(
            message="Select action:",
            choices=(
                Choice(True, name="Encrypt message"),
                Choice(False, name="Decrypt message")
            )
        ).execute()
        if encrypt_mode:
            result = encrypt_caesar(message, self.shift_value)
        else:
            result = decrypt_caesar(message, self.shift_value)
        color_print([("green", "Result:"), ("", " "), ("", result)])

    def ask_action(self) -> str:
        action_to_perform = inquirer.select(
            message="Select next action:",
            choices=(
                self.NEW_MESSAGE_ACTION,
                self.CHANGE_KEY_ACTION,
                self.EXIT_ACTION
            )
        ).execute()
        return action_to_perform


class VigenereInterface:
    EXIT_ACTION = "Exit Vigenere cipher"
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
        key = inquirer.text(
            message="Enter key:",
            validate=lambda x: x.strip().isalpha(),
            invalid_message="Key must a sequence of letters"
        ).execute()
        self.key = key.strip()
    
    def encrypt_or_decrypt_message(self):
        message = inquirer.text(
            message="Enter message to encrypt/decrypt:",
            multiline=True
        ).execute()
        encrypt_mode = inquirer.select(
            message="Select action:",
            choices=(
                Choice(True, name="Encrypt message"),
                Choice(False, name="Decrypt message")
            )
        ).execute()
        if encrypt_mode:
            result = encrypt_vigenere(message, self.key)
        else:
            result = decrypt_vigenere(message, self.key)
        color_print([("green", "Result:"), ("", " "), ("", result)])

    def ask_action(self) -> str:
        action_to_perform = inquirer.select(
            message="Select next action:",
            choices=(
                self.NEW_MESSAGE_ACTION,
                self.CHANGE_KEY_ACTION,
                self.EXIT_ACTION
            )
        ).execute()
        return action_to_perform


if __name__ == "__main__":
    CaesarInterface().run()
    VigenereInterface().run()
