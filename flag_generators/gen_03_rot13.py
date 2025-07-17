#!/usr/bin/env python3

from pathlib import Path
import random
import codecs
import sys
from flag_generators.flag_helpers import FlagUtils


class ROT13FlagGenerator:
    """
    Generator for the ROT13 cipher challenge.
    Embeds real and fake flags into a cipher.txt file.
    """
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

    @staticmethod
    def rot13(text: str) -> str:
        """Apply ROT13 cipher to the given text."""
        return codecs.encode(text, "rot_13")

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Create cipher.txt in the challenge folder with ROT13-encoded flags.
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

            # Apply ROT13 to each flag
            encoded_flags = [self.rot13(flag) for flag in all_flags]

            # Write to cipher.txt
            cipher_file.write_text(
                "Multiple codes recovered. Only one fits the agency’s flag format.\n\n" +
                "\n".join(f"- {flag}" for flag in encoded_flags)
            )
            print(f"📝 cipher.txt created with {len(all_flags)} ROT13-encoded flags.")

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate flags and embed them into cipher.txt.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        # Ensure real flag isn’t duplicated accidentally
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
