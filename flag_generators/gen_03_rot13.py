#!/usr/bin/env python3

from pathlib import Path
import random
import codecs
import sys
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag

# === Helper: Find Project Root ===
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

# === Resolve Paths ===
PROJECT_ROOT = find_project_root()

def rot13(text: str) -> str:
    """Apply ROT13 cipher to the given text."""
    return codecs.encode(text, "rot_13")

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create cipher.txt in the challenge folder with ROT13-encoded flags.
    """
    cipher_file = challenge_folder / "cipher.txt"

    try:
        # Check if target directory exists
        if not challenge_folder.exists():
            raise FileNotFoundError(f"❌ Challenge folder not found: {challenge_folder.relative_to(PROJECT_ROOT)}")

        # Combine and shuffle flags
        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)

        # Apply ROT13 to each flag
        encoded_flags = [rot13(flag) for flag in all_flags]

        # Write to cipher.txt
        cipher_file.write_text(
            "Multiple codes recovered. Only one fits the agency’s flag format.\n\n" +
            "\n".join(f"- {flag}" for flag in encoded_flags)
        )
        print(f"📝 cipher.txt created with {len(all_flags)} ROT13-encoded flags.")

    except PermissionError:
        print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(PROJECT_ROOT)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate a real flag and fake flags, embed them into cipher.txt,
    and return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure real flag isn’t duplicated accidentally
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
