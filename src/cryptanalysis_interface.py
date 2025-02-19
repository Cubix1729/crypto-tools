from InquirerPy import inquirer
from cryptanalysis_classical_ciphers import (
    break_caesar,
    break_affine,
    break_vigenere,
    key_length,
)
from classical_ciphers import decrypt_caesar, decrypt_affine, decrypt_vigenere
from InquirerPy.utils import color_print


class CaesarCryptanalysisInterface:
    EXIT_ACTION = "Exit Caesar cipher breaking"
    NEW_CIPHERTEXT_ACTION = "Enter new ciphertext to break"

    def run(self):
        self.enter_ciphertext()
        while True:
            action = self.ask_action()
            match action:
                case self.EXIT_ACTION:
                    break
                case self.NEW_CIPHERTEXT_ACTION:
                    self.enter_ciphertext()

    def enter_ciphertext(self):
        ciphertext = inquirer.text(
            message="Enter ciphertext to break:",
            multiline=True,
            validate=lambda x: len(x) != 0,
            invalid_message="Ciphertext must not be empty",
        ).execute()
        shift_found = break_caesar(ciphertext)
        color_print(
            (
                ["green", "Shift value found: "],
                ["#d097ff", str(shift_found) + "\n"],
                ["green", "Decrypted text: "],
                ["#d097ff", decrypt_caesar(ciphertext, shift_found) + "\n"],
                ["grey", "Results may be inaccurate for short messages"],
            )
        )

    def ask_action(self) -> str:
        action_to_perform = inquirer.select(
            message="Select next action:", choices=(self.NEW_CIPHERTEXT_ACTION, self.EXIT_ACTION)
        ).execute()
        return action_to_perform


class AffineCryptanalysisInterface(CaesarCryptanalysisInterface):
    EXIT_ACTION = "Exit affine cipher breaking"

    def enter_ciphertext(self):
        ciphertext = inquirer.text(
            message="Enter ciphertext to break:",
            multiline=True,
            validate=lambda x: len(x) != 0,
            invalid_message="Ciphertext must not be empty",
        ).execute()
        a_found, b_found = break_affine(ciphertext)
        color_print(
            (
                ["green", "'a' value found: "],
                ["#d097ff", str(a_found) + "\n"],
                ["green", "'b' value found: "],
                ["#d097ff", str(b_found) + "\n"],
                ["green", "Decrypted text: "],
                ["#d097ff", decrypt_affine(ciphertext, a_found, b_found) + "\n"],
                ["grey", "Results may be inaccurate for short messages"],
            )
        )


class KeyLengthFindingInterface(CaesarCryptanalysisInterface):
    EXIT_ACTION = "Exit Vigenere/Beaufort key length finding"
    NEW_CIPHERTEXT_ACTION = "Analyse new ciphertext"

    def enter_ciphertext(self):
        ciphertext = inquirer.text(
            message="Enter ciphertext to analyse:",
            multiline=True,
            validate=lambda x: len(x) != 0,
            invalid_message="Ciphertext must not be empty",
        ).execute()
        min_key_len = inquirer.number("Enter minimum key length:").execute()
        max_key_len = inquirer.number("Enter maximum key length:").execute()
        key_len_found = key_length(ciphertext, int(min_key_len), int(max_key_len))
        color_print(
            (
                ["green", "Key length found: "],
                ["#d097ff", str(key_len_found) + "\n"],
                ["grey", "Results may be inaccurate for short messages"],
            )
        )


class VigenereCryptanalysisInterface(CaesarCryptanalysisInterface):
    EXIT_ACTION = "Exit Vigenere breaking"

    def enter_ciphertext(self):
        ciphertext = inquirer.text(
            message="Enter ciphertext to break:",
            multiline=True,
            validate=lambda x: len(x) != 0,
            invalid_message="Ciphertext must not be empty",
        ).execute()
        key_len = int(inquirer.number("Enter presumed key length:").execute())
        key_found = break_vigenere(ciphertext, key_len)
        color_print(
            (
                ["green", "Key found: "],
                ["#d097ff", key_found + "\n"],
                ["green", "Decrypted text: "],
                ["#d097ff", decrypt_vigenere(ciphertext, key_found) + "\n"],
                ["grey", "Results may be inaccurate for short messages"],
            )
        )


class GlobalCryptanalysisInterface:
    EXIT_ACTION = "Exit cryptanalysis menu"
    CAESAR_ACTION = "Break Caesar cipher"
    AFFINE_ACTION = "Break affine cipher"
    KEY_LENGTH_ACTION = "Find Vigenere/Beaufort key length"
    VIGENERE_ACTION = "Break Vigenere cipher with key length"

    def run(self):
        try:
            while True:
                action = self.ask_action()
                try:
                    match action:
                        case self.EXIT_ACTION:
                            break
                        case self.CAESAR_ACTION:
                            CaesarCryptanalysisInterface().run()
                        case self.VIGENERE_ACTION:
                            VigenereCryptanalysisInterface().run()
                        case self.KEY_LENGTH_ACTION:
                            KeyLengthFindingInterface().run()
                        case self.AFFINE_ACTION:
                            AffineCryptanalysisInterface().run()
                except KeyboardInterrupt:
                    pass
        except KeyboardInterrupt:
            pass

    def ask_action(self):
        action_to_perform = inquirer.select(
            "Select program:",
            choices=(
                self.CAESAR_ACTION,
                self.AFFINE_ACTION,
                self.KEY_LENGTH_ACTION,
                self.VIGENERE_ACTION,
                self.EXIT_ACTION,
            ),
        ).execute()
        return action_to_perform


if __name__ == "__main__":
    VigenereCryptanalysisInterface().run()
    CaesarCryptanalysisInterface().run()
    AffineCryptanalysisInterface().run()
    KeyLengthFindingInterface().run()
