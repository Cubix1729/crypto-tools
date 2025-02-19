from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from enigma_machine import EnigmaI, EnigmaM3, EnigmaM4
from helper_functions import print_result
import random
import string
import copy


class EnigmaInterface:
    EXIT_ACTION = "Exit Enigma simulator"
    NEW_MESSAGE_ACTION = "Encrypt/decrypt new message"
    CHANGE_SETTINGS_ACTION = "Change Enigma settings"

    ENIGMA_MODELS_CHOICES = (
        Choice(EnigmaI, name="Enigma I"),
        Choice(EnigmaM3, name="Enigma M3"),
        Choice(EnigmaM4, name="Enigma M4"),
    )
    ROTORS_POSSIBLE = {
        EnigmaI: ["I", "II", "III", "IV", "V"],
        EnigmaM3: ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"],
        EnigmaM4: ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"],
    }
    REFLECTORS_POSSIBLE = {EnigmaI: ["A", "B", "C"], EnigmaM3: ["B", "C"], EnigmaM4: ["BTHIN", "CTHIN"]}
    CHANGE_SETTINGS_CHOICES = (
        "Enigma model",
        "Rotors",
        "Reflector",
        "Ring settings",
        "Starting positions",
        "Plugboard",
    )

    def run(self):
        self.ask_enigma_model()
        self.ask_rotors()
        self.ask_reflector()
        self.ask_ring_settings()
        self.ask_starting_positions()
        self.ask_plugboard()
        self.enter_message()
        while True:
            action = self.ask_next_action()
            if action == self.EXIT_ACTION:
                break
            elif action == self.NEW_MESSAGE_ACTION:
                self.enter_message()
            elif action == self.CHANGE_SETTINGS_ACTION:
                self.change_setting()

    def ask_enigma_model(self):
        enigma_model = inquirer.select(message="Select Enigma model:", choices=self.ENIGMA_MODELS_CHOICES).execute()
        self.enigma_model = enigma_model

    def ask_rotors(self):
        self.rotors = []
        if self.enigma_model == EnigmaM4:
            leftmost_rotor = inquirer.select(
                message="Select 1st (leftmost) rotor:", choices=("Beta", "Gamma")
            ).execute()
            self.rotors.append(leftmost_rotor.upper())
        # 'Last' three rotors
        possible_rotor_choices: list = copy.deepcopy(self.ROTORS_POSSIBLE[self.enigma_model])
        for rotor_index in range(3):
            if rotor_index == 0 and self.enigma_model != EnigmaM4:
                message = "Select 1st (leftmost) rotor:"
            else:
                message = "Select next rotor:"
            rotor_chosen = inquirer.select(message=message, choices=possible_rotor_choices).execute()
            self.rotors.append(rotor_chosen)
            possible_rotor_choices.remove(rotor_chosen)

    def ask_reflector(self):
        reflector = inquirer.select(
            message="Select the reflector:", choices=self.REFLECTORS_POSSIBLE[self.enigma_model]
        ).execute()
        self.reflector = reflector

    def ask_ring_settings(self):
        self.ring_settings = []
        for index in range(len(self.rotors)):
            ring_setting = inquirer.text(
                message=f"Enter ring setting for rotor {index + 1} (letter):",
                validate=lambda x: x.strip().isalpha() and len(x.strip()) == 1,
                invalid_message="Ring setting must be a letter",
            ).execute()
            self.ring_settings.append(ring_setting.strip().upper())

    def ask_starting_positions(self):
        self.starting_positions = []
        for index in range(len(self.rotors)):
            ring_setting = inquirer.text(
                message=f"Enter starting position for rotor {index + 1} (letter):",
                validate=lambda x: x.strip().isalpha() and len(x.strip()) == 1,
                invalid_message="Starting position must be a letter",
            ).execute()
            self.starting_positions.append(ring_setting.strip().upper())

    def ask_plugboard(self, ask_confirmation=True):
        if ask_confirmation:
            plugboard_used = inquirer.confirm(message="Add plugboard connections?").execute()
        else:
            plugboard_used = True
        if plugboard_used:
            self.plugboard = {}
            while True:
                connection_example = random.choice(string.ascii_uppercase)
                alphabet_without_first_plug = list(string.ascii_uppercase)
                alphabet_without_first_plug.remove(connection_example)
                connection_example += random.choice(alphabet_without_first_plug)
                plugboard_connection = inquirer.text(
                    message="Enter plugboard connection:",
                    instruction=f"(ex: {connection_example})",
                    long_instruction="Control-Z to skip and finish entering plugboard configuration",
                    validate=lambda x: x.strip().isalpha() and len(x.strip()) == 2,
                    invalid_message="Invalid input: plugboard connection must consist of two letters",
                    mandatory=False,
                ).execute()
                if plugboard_connection is None:
                    break
                else:
                    plugboard_connection = plugboard_connection.strip().upper()
                    key = plugboard_connection[0]
                    value = plugboard_connection[1]
                    if self.plugboard.get(key) == value and self.plugboard.get(value) == key:
                        continue
                    if key in self.plugboard.keys() or value in self.plugboard.keys():
                        color_print((["red", "Invalid (incompatible) plug"],))
                    self.plugboard[key] = value
                    self.plugboard[value] = key
        else:
            self.plugboard = {}

    def enter_message(self):
        message_to_encrypt_or_decrypt = inquirer.text(
            message="Enter message to encrypt or decrypt:", multiline=True, mandatory=False
        ).execute()

        enigma_machine_to_use = self.enigma_model(
            rotors=self.rotors,
            ring_settings=self.ring_settings,
            reflector=self.reflector,
            plugboard=self.plugboard,
            starting_positions=self.starting_positions,
        )
        encrypted_or_decrypted_message = enigma_machine_to_use.encrypt(message_to_encrypt_or_decrypt)
        print_result(encrypted_or_decrypted_message)

    def ask_next_action(self) -> str:
        action_to_perform = inquirer.select(
            message="Select next action:",
            choices=(self.NEW_MESSAGE_ACTION, self.CHANGE_SETTINGS_ACTION, self.EXIT_ACTION),
        ).execute()
        return action_to_perform

    def change_setting(self):
        setting_to_change = inquirer.select(
            message="Select setting to change:",
            choices=("Enigma model", "Rotors", "Reflector", "Ring settings", "Starting positions", "Plugboard"),
        ).execute()
        match setting_to_change:
            case "Enigma model":
                self.ask_enigma_model()
                self.ask_rotors()
                self.ask_reflector()
                self.ask_ring_settings()
                self.ask_starting_positions()
            case "Rotors":
                self.ask_rotors()
            case "Reflector":
                self.ask_reflector()
            case "Ring settings":
                self.ask_ring_settings()
            case "Starting positions":
                self.ask_starting_positions()
            case "Plugboard":
                self.ask_plugboard(ask_confirmation=False)


if __name__ == "__main__":
    EnigmaInterface().run()
