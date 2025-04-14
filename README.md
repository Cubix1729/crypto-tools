# CryptoTools

CryptoTools is a terminal user interface implementing classical ciphers like the Caesar or Vigenere cipher, as well as the Enigma machine.
It has some cryptanalysis features for breaking simple ciphers.

![alt text](./images/main_menu_image.png "Main menu")

![alt text](./images/enigma_example_image.png "Enigma interface")

It currently supports:
 - Enigma machine
 - Caesar cipher
 - Affine cipher
 - Vigenere cipher and its variants: Beaufort cipher and autokey/autoclave cipher
 - Index of coincidence calculating
 - Cryptanalysis of several ciphers:
    - Caesar cipher
    - Affine cipher
    - Vigenere cipher (including key length finding)

## Installation

```
git clone https://github.com/Cubix1729/crypto-tools.git
cd crypto-tools
pip install -r requirements.txt
```

To run the CLI:

```
python ./src/global_interface.py
```

## Usage

Use the `up` and `down` arrow keys to navigate in a menu and press `enter` to confirm a choice.\
Pressing `Control-C` will exit the current interface.

## Dependencies

 - `InquirerPy` used for making the interactive command-line interface

`black` is used for code formatting (with line length 120).

[dCode](https://www.dcode.fr/en) website was really useful for verifying my results and finding letters/bigrams/trigrams frequencies.