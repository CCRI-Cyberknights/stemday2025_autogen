#!/usr/bin/env python3

from pathlib import Path
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class VigenereFlagGenerator:
    """
    Generator for the Vigenère cipher challenge.
    Encodes an intercepted transmission (including flags) into cipher.txt.
    """
    VIGENERE_KEY = "login"

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()

    @staticmethod
    def find_project_root() -> Path:
        """
        Walk up directories until .ccri_ctf_root is found.
        """
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    @classmethod
    def vigenere_encrypt(cls, plaintext: str, key: str = None) -> str:
        """
        Encrypt plaintext using Vigenère cipher with the given key.
        """
        key = (key or cls.VIGENERE_KEY).upper()
        result = []
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

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Create cipher.txt in the challenge folder with a Vigenère-encrypted message.
        """
        cipher_file = challenge_folder / "cipher.txt"

        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            # Combine and shuffle flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            # Build plaintext message
            message = (
                "Transmission Start\n"
                "------------------------\n"
                "To: LIBER8 Command Node\n"
                "From: Field Unit 7\n\n"
                "Status report: Flag candidates identified during operation. "
                "Data has been encoded for secure transit.\n\n"
                "Candidates:\n"
                + "\n".join(f"- {flag}" for flag in all_flags)
                + "\n\nVerify the true flag before submission.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            # Encrypt the entire message
            encrypted_message = self.vigenere_encrypt(message)

            # Write to cipher.txt
            cipher_file.write_text(encrypted_message)
            print(f"📝 {cipher_file.relative_to(self.project_root)} created with Vigenère-encrypted transmission.")

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error during embedding: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate a real flag and embed it into cipher.txt.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        # Ensure no accidental duplicate
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
