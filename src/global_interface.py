from enigma_interface import EnigmaInterface
from classical_ciphers_interface import (
    CaesarInterface,
    VigenereInterface,
    BeaufortInterface,
    AutokeyInterface,
    AffineInterface,
    IndexOfCoincidenceInterface,
)
from cryptanalysis_interface import GlobalCryptanalysisInterface
from InquirerPy import inquirer
from InquirerPy.utils import color_print


TEXT_LOGO = r"""   ______                 __           ______            __
  / ____/______  ______  / /_____     /_  __/___  ____  / /____
 / /   / ___/ / / / __ \/ __/ __ \     / / / __ \/ __ \/ / ___/
/ /___/ /  / /_/ / /_/ / /_/ /_/ /    / / / /_/ / /_/ / (__  )
\____/_/   \__, / .___/\__/\____/    /_/  \____/\____/_/____/
          /____/_/
"""


class CryptoToolsInterface:
    EXIT_ACTION = "Exit program"
    ENIGMA_ACTION = "Enigma machine"
    CAESAR_ACTION = "Caesar cipher"
    VIGENERE_ACTION = "Vigenere cipher"
    BEAUFORT_ACTION = "Beaufort cipher"
    AUTOKEY_ACTION = "Autokey cipher"
    AFFINE_ACTION = "Affine cipher"
    IoC_ACTION = "Index of coincidence"
    CRYPTANALYSIS_ACTION = "Cryptanalysis menu"

    def run(self):
        color_print((["#2acafd", TEXT_LOGO],))
        try:
            while True:
                action = self.ask_action()
                try:
                    match action:
                        case self.EXIT_ACTION:
                            break
                        case self.ENIGMA_ACTION:
                            EnigmaInterface().run()
                        case self.CAESAR_ACTION:
                            CaesarInterface().run()
                        case self.VIGENERE_ACTION:
                            VigenereInterface().run()
                        case self.BEAUFORT_ACTION:
                            BeaufortInterface().run()
                        case self.AUTOKEY_ACTION:
                            AutokeyInterface().run()
                        case self.AFFINE_ACTION:
                            AffineInterface().run()
                        case self.IoC_ACTION:
                            IndexOfCoincidenceInterface().run()
                        case self.CRYPTANALYSIS_ACTION:
                            GlobalCryptanalysisInterface().run()
                except KeyboardInterrupt:
                    pass
        except KeyboardInterrupt:
            pass

    def ask_action(self):
        action_to_perform = inquirer.select(
            "Select program:",
            choices=(
                self.ENIGMA_ACTION,
                self.CAESAR_ACTION,
                self.VIGENERE_ACTION,
                self.BEAUFORT_ACTION,
                self.AUTOKEY_ACTION,
                self.AFFINE_ACTION,
                self.IoC_ACTION,
                self.CRYPTANALYSIS_ACTION,
                self.EXIT_ACTION,
            ),
        ).execute()
        return action_to_perform


if __name__ == "__main__":
    CryptoToolsInterface().run()
