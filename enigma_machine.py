from helper_functions import *
import string


class Enigma:
    """A class used to represent an Enigma machine"""

    def __init__(
        self,
        rotors: list[str],
        rotor_notches: list[int | str | list[int | str]],
        ring_settings: list[int | str],
        reflector: str,
        plugboard: dict,
        starting_positions: list[int] | str = None,
        preserve_non_alphabetic_characters: bool = False,
    ):
        """Parameters:
        rotors: the rotors of the machine from left to right (represented by strings of 26 letters)
        rotor_notches: the respective placements of the notches of the different rotors
        ring_settings: the respective ring settings for each rotor
        reflector: the reflector used (in the same format as the rotors)
        plugboard: the steckerbrett used

        Optional:
        starting_positions: the respective rotor starting positions (if it is not precised, it will have to be precised when encrypting the first message)
        preserve_non_alphabetic_characters: whether formatting should be removed in the crypted messages (defaults to False)

        Note: rotor_notches, ring_settings and starting_positions are precised as letters or letter indexes with A=1
        """

        # We first verify the values given
        if not len(rotors) in (3, 4):
            raise ValueError("rotors must have length 3 or 4")

        for rotor in rotors:
            if len(rotor) != 26:
                raise ValueError("rotors must have length 26")

        if len(rotors) != len(rotor_notches):
            raise ValueError("invalid length for rotor_notches")

        if len(rotors) != len(ring_settings):
            raise ValueError("invalid length for ring_settings")

        if len(reflector) != 26:
            raise ValueError("reflector must have length 26")

        if starting_positions is not None:
            if len(starting_positions) != len(rotors):
                raise ValueError("invalid length for starting_positions")

        # We convert left-to-right indexing to right-to-left as it is more practical
        self.rotor_wirings = list(reversed(rotors))
        self.rotors = list(reversed(rotors))
        self.rotor_notches = list(reversed(rotor_notches))
        self.ring_positions = list(reversed(ring_settings))
        self.rotor_positions = list(reversed(starting_positions))
        self.starting_positions = list(reversed(starting_positions))

        self.plugboard = plugboard
        self.reflector = reflector

        self.preserve_non_alphabetic_characters = preserve_non_alphabetic_characters

        # We convert the notches, ring and rotor positions to integers (letter indexes)
        for index, ring_position in enumerate(self.ring_positions):
            if isinstance(ring_position, str):
                self.ring_positions[index] = letter_index(ring_position)

        if self.rotor_positions is not None:
            for index, rotor_position in enumerate(self.rotor_positions):
                if isinstance(rotor_position, str):
                    self.rotor_positions[index] = letter_index(rotor_position)
            self.starting_positions = self.rotor_positions

        for index, rotor_notch in enumerate(self.rotor_notches):
            new_rotor_notch = []
            for notch in rotor_notch:
                if isinstance(notch, str):
                    new_rotor_notch.append(letter_index(notch))
                else:
                    new_rotor_notch.append(notch)
            self.rotor_notches[index] = new_rotor_notch

        # Reversing the plugboard connections
        new_plugboard = {}
        for key, value in self.plugboard.items():
            if new_plugboard.get(key) == value and new_plugboard.get(value) == key:
                continue
            if key in new_plugboard.keys() or value in new_plugboard.keys():
                raise ValueError("invalid plugboard: incompatible connections found")
            new_plugboard[key] = value
            new_plugboard[value] = key
        self.plugboard = new_plugboard

    def has_to_step(self, rotor_index: int) -> bool:
        """Returns True if the given rotor has to step and False otherwise"""
        if rotor_index == 0:
            return True

        if rotor_index in (1, 2):
            rotor_notch = self.rotor_notches[rotor_index - 1]
            if isinstance(rotor_notch, int):  # there is only one rotor notch
                return self.rotor_positions[rotor_index - 1] == rotor_notch

            else:  # there are several notches for this rotor
                return self.rotor_positions[rotor_index - 1] in rotor_notch

    def step_rotor(self, rotor_index: int, num_steps: int = 1):
        """Steps the rotor given"""
        self.rotor_positions[rotor_index] = to_number_between_1_and_26(self.rotor_positions[rotor_index] + num_steps)
        self.rotors[rotor_index] = rotate_rotor(self.rotors[rotor_index], offset=num_steps)

    def step_rotors(self):
        """Steps the rotors of the Enigma machine"""

        # Rotation of the leftmost rotor for 3 rotor Enigma
        if self.has_to_step(rotor_index=2):
            self.step_rotor(rotor_index=2)
            # Double-stepping implementation
            self.step_rotor(rotor_index=1)

        # Rotation of the second rightmost rotor (middle one for 3 rotors machines)
        if self.has_to_step(rotor_index=1):
            self.step_rotor(rotor_index=1)

        # Rotation of the rightmost rotor
        self.step_rotor(rotor_index=0)

        # If there is one the 4th rotor doesn't turn

    def initialise_rotors(self):
        for i in range(len(self.rotors)):
            rotor_wiring = self.rotor_wirings[i]
            ring_position = self.ring_positions[i]
            starting_position = self.starting_positions[i]

            self.rotors[i] = rotate_rotor(self.rotor_wirings[i], offset=starting_position - ring_position)

    def encrypt(self, text: str, starting_positions=None) -> str:
        """Returns the encrypted text from the one given
        If starting_positions is not precised, the ones given in the beginning will be used"""
        if starting_positions is not None:
            if len(starting_positions) != len(self.rotors):
                raise ValueError("invalid length for starting_positions")
            self.rotor_positions = starting_positions
        else:
            self.rotor_positions = self.starting_positions

        if self.rotor_positions is None:
            raise ValueError("starting_positions must be precised")

        self.initialise_rotors()

        list_of_encrypted_letters = []

        if self.preserve_non_alphabetic_characters:
            text = text.upper()
        else:
            text = to_upper_case_without_punctuation_or_spaces(text)

        for letter in to_upper_case_without_punctuation_or_spaces(text):
            if letter not in string.ascii_uppercase:  # the "letter" to encrypt isn't a letter
                list_of_encrypted_letters.append(letter)
                continue

            # We step the rotors once
            self.step_rotors()

            # The letter passes through the plugboard
            letter = self.plugboard.get(letter, letter)

            # It then passes through the rotors
            for i in range(len(self.rotors)):
                current_rotor = self.rotors[i]
                letter = current_rotor[letter_index(letter) - 1]
                current_rotor_position = self.rotor_positions[i]
                current_ring_position = self.ring_positions[i]
                current_rotor_offset = to_number_between_1_and_26(current_rotor_position - current_ring_position)
                letter = shift_letter(letter, -current_rotor_offset)

            # It passes through the reflector
            letter = self.reflector[letter_index(letter) - 1]

            # It passes back again through the rotors
            for i in range(len(self.rotors) - 1, -1, -1):
                current_rotor = self.rotors[i]
                current_rotor_position = self.rotor_positions[i]
                current_ring_position = self.ring_positions[i]
                current_rotor_offset = to_number_between_1_and_26(current_rotor_position - current_ring_position)
                letter = shift_letter(letter, current_rotor_offset)
                letter = letter_from_index(current_rotor.index(letter) + 1)

            # It returns through the plugboard
            letter = self.plugboard.get(letter, letter)

            list_of_encrypted_letters.append(letter)

        return "".join(list_of_encrypted_letters)

    def decrypt(self, text: str, starting_positions=None):
        """Returns the decrypted text from the one given
        If starting_positions is not precised, the ones given in the beginning will be used"""
        return self.encrypt(text, starting_positions)


class EnigmaI(Enigma):
    """A class representing the Enigma I machine with its rotors I to V and its reflectors A, B and C"""

    ROTORS = {
        "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        "V": "VZBRGITYUPSDNHLXAWMJQOFECK",
    }

    REFLECTORS = {
        "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
        "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    }

    NOTCHES = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z"}

    def __init__(
        self,
        rotors,
        ring_settings,
        plugboard,
        reflector="B",
        starting_positions=None,
        preserve_non_alphabetic_characters=False,
    ):
        if len(rotors) != 3:
            raise ValueError("this Enigma has 3 rotors")
        if len(ring_settings) != 3:
            raise ValueError("this Enigma has 3 rotors")
        if starting_positions is not None:
            if len(starting_positions) != 3:
                raise ValueError("this Enigma has 3 rotors")

        rotor_wirings = []
        notch_positions = []
        for rotor in rotors:
            try:
                rotor_wirings.append(self.ROTORS[rotor])
                notch_positions.append(self.NOTCHES[rotor])
            except KeyError:
                raise ValueError(f"invalid rotor name '{rotor}'")

        try:
            reflector_wiring = self.REFLECTORS[reflector]
        except KeyError:
            raise ValueError(f"invalid reflector name '{reflector}'")

        super().__init__(
            rotors=rotor_wirings,
            rotor_notches=notch_positions,
            ring_settings=ring_settings,
            reflector=reflector_wiring,
            plugboard=plugboard,
            starting_positions=starting_positions,
            preserve_non_alphabetic_characters=preserve_non_alphabetic_characters,
        )


class EnigmaM3(EnigmaI):
    """A class representing the naval Enigma M3 machine"""

    ROTORS = {
        "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        "V": "VZBRGITYUPSDNHLXAWMJQOFECK",
        "VI": "JPGVOUMFYQBENHZRDKASXLICTW",
        "VII": "NZJHGRCXMYSWBOUFAIVLPEKQDT",
        "VIII": "FKQHTLXOCBJSPDZRAMEWNIUYGV",
    }

    REFLECTORS = {
        "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    }

    NOTCHES = {
        "I": "Q",
        "II": "E",
        "III": "V",
        "IV": "J",
        "V": "Z",
        "VI": "ZM",
        "VII": "ZM",
        "VIII": "ZM",
    }


class EnigmaM4(EnigmaM3):
    """A class representing the naval Enigma M4 machine with its rotors I to VIII, BETA and GAMMA and its reflectors A, B and C"""

    ROTORS = {
        "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        "V": "VZBRGITYUPSDNHLXAWMJQOFECK",
        "VI": "JPGVOUMFYQBENHZRDKASXLICTW",
        "VII": "NZJHGRCXMYSWBOUFAIVLPEKQDT",
        "VIII": "FKQHTLXOCBJSPDZRAMEWNIUYGV",
    }

    LEFTMOST_ROTORS = {"BETA": "LEYJVCNIXWPBQMDRTAKZGFUHOS", "GAMMA": "FSOKANUERHMBTIYCWLQPZXVGJD"}

    REFLECTORS = {
        "BTHIN": "ENKQAUYWJICOPBLMDXZVFTHRGS",
        "CTHIN": "RDOBJNTKVEHMLFCWZAXGYIPSUQ",
    }

    NOTCHES = {
        "I": "Q",
        "II": "E",
        "III": "V",
        "IV": "J",
        "V": "Z",
        "VI": "ZM",
        "VII": "ZM",
        "VIII": "ZM",
    }

    LEFTMOST_ROTOR_NOTCHES = {"BETA": "", "GAMMA": ""}

    def __init__(
        self,
        rotors,
        ring_settings,
        plugboard,
        reflector="B",
        starting_positions=None,
        preserve_non_alphabetic_characters=False,
    ):
        if len(rotors) != 4:
            raise ValueError("this Enigma has 4 rotors")
        if len(ring_settings) != 4:
            raise ValueError("this Enigma has 4 rotors")
        if starting_positions is not None:
            if len(starting_positions) != 4:
                raise ValueError("this Enigma has 4 rotors")

        rotor_wirings = []
        notch_positions = []
        for rotor_index, rotor in enumerate(rotors):
            if rotor_index == 0:  # The rotor is in leftmost position
                try:
                    rotor_wirings.append(self.LEFTMOST_ROTORS[rotor])
                    notch_positions.append(self.LEFTMOST_ROTOR_NOTCHES[rotor])
                except KeyError:
                    raise ValueError(f"invalid rotor '{rotor}' in leftmost position")

            else:
                try:
                    rotor_wirings.append(self.ROTORS[rotor])
                    notch_positions.append(self.NOTCHES[rotor])
                except KeyError:
                    raise ValueError(f"invalid rotor name '{rotor}'")

        try:
            reflector_wiring = self.REFLECTORS[reflector]
        except KeyError:
            raise ValueError(f"invalid reflector name '{reflector}'")

        Enigma.__init__(
            self,
            rotors=rotor_wirings,
            rotor_notches=notch_positions,
            ring_settings=ring_settings,
            reflector=reflector_wiring,
            plugboard=plugboard,
            starting_positions=starting_positions,
            preserve_non_alphabetic_characters=preserve_non_alphabetic_characters,
        )
