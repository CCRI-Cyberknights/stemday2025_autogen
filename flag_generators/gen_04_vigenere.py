#!/usr/bin/env python3

from pathlib import Path
import random
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

VIGENERE_KEY = "login"

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using Vigenère cipher with given key.
    """
    result = []
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            pi = ord(char) - offset
            ki = ord(key[i % key_length]) - ord('A')
            ci = (pi + ki) % 26
            result.append(chr(ci + offset))
        else:
            result.append(char)  # Leave non-alpha chars unchanged
    return ''.join(result)

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create cipher.txt in the challenge folder with Vigenère-encrypted flags.
    """
    cipher_file = challenge_folder / "cipher.txt"

    # Combine and shuffle flags
    all_flags = fake_flags + [real_flag]
    random.shuffle(all_flags)

    # Encrypt each flag
    encrypted_flags = [vigenere_encrypt(flag, VIGENERE_KEY) for flag in all_flags]

    # Write to cipher.txt
    preamble = (
        "Agency decrypted several possible code fragments from the recovered file.\n\n"
        "Here are the extracted flag-like values:\n"
    )
    postamble = (
        "\nOnly one of these follows the official agency flag format.\n\n"
        "Cross-check carefully before submitting."
    )

    cipher_file.write_text(
        preamble +
        "\n".join(f"- {flag}" for flag in encrypted_flags) +
        postamble
    )

    print(f"📝 cipher.txt created with {len(all_flags)} Vigenère-encrypted flags.")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate a real flag and fake flags, embed them into cipher.txt,
    and return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
