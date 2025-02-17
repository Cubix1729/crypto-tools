from enigma_interface import EnigmaInterface
from classical_ciphers_interface import CaesarInterface, VigenereInterface, AffineInterface
from InquirerPy import inquirer
from InquirerPy.utils import color_print
from pyfiglet import Figlet


class GlobalInterface:
    EXIT_ACTION = "Exit program"
    ENIGMA_ACTION = "Enigma machine"
    CAESAR_ACTION = "Caesar cipher"
    VIGENERE_ACTION = "Vigenere cipher"
    AFFINE_ACTION = "Affine cipher"

    def run(self):
        font = Figlet(font="slant")
        color_print((["#2acafd", font.renderText("Cryptography")],))
        while True:
            action = self.ask_action()
            if action == self.EXIT_ACTION:
                break
            elif action == self.ENIGMA_ACTION:
                EnigmaInterface().run()
            elif action == self.CAESAR_ACTION:
                CaesarInterface().run()
            elif action == self.VIGENERE_ACTION:
                VigenereInterface.run()
            elif action == self.AFFINE_ACTION:
                AffineInterface().run()

    def ask_action(self):
        action_to_perform = inquirer.select(
            "Select program:",
            choices=(
                self.ENIGMA_ACTION,
                self.CAESAR_ACTION,
                self.VIGENERE_ACTION,
                self.AFFINE_ACTION,
                self.EXIT_ACTION,
            ),
        ).execute()
        return action_to_perform


if __name__ == "__main__":
    GlobalInterface().run()
