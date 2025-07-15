#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import base64
import sys
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag

# Path to master wordlist template (dev copy in flag_generators/)
WORDLIST_TEMPLATE = Path(__file__).parent / "wordlist.txt"

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create wordlist.txt and password-protected secret.zip containing message_encoded.txt.
    """
    try:
        # Check if challenge folder exists
        if not challenge_folder.exists():
            raise FileNotFoundError(f"❌ Challenge folder not found: {challenge_folder}")

        # Check if wordlist template exists
        if not WORDLIST_TEMPLATE.exists():
            raise FileNotFoundError(f"❌ Wordlist template missing: {WORDLIST_TEMPLATE}")

        # Load master wordlist
        all_passwords = WORDLIST_TEMPLATE.read_text().splitlines()
        if not all_passwords:
            raise ValueError("❌ Wordlist template is empty!")

        # Randomly pick a password from the list
        correct_password = random.choice(all_passwords)

        # Copy wordlist.txt into challenge folder
        wordlist_file = challenge_folder / "wordlist.txt"
        wordlist_file.write_text("\n".join(all_passwords))

        # Create message_encoded.txt (base64-encoded flags)
        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)
        message = (
            "Mission Debrief:\n\n"
            "Encrypted transmission recovered from target machine.\n"
            "Analysis reveals five potential keys, but only one fits agency format.\n\n"
            "Decoded entries:\n" +
            "\n".join(f"- {flag}" for flag in all_flags) +
            "\n\nProceed with caution."
        )
        message_encoded = base64.b64encode(message.encode("utf-8")).decode("utf-8")

        # Save message_encoded.txt temporarily
        encoded_file = challenge_folder / "message_encoded.txt"
        encoded_file.write_text(message_encoded)

        # Create password-protected secret.zip
        zip_file = challenge_folder / "secret.zip"
        result = subprocess.run(
            ["zip", "-P", correct_password, str(zip_file), str(encoded_file)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"❌ Zip failed: {result.stderr.strip()}")

        # Clean up temporary file
        encoded_file.unlink()
        print(f"🗝️ wordlist.txt and 🔒 secret.zip created with correct password: {correct_password}")

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except PermissionError as e:
        print(f"❌ Permission error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate a real flag and fake flags, embed them into secret.zip and wordlist.txt,
    and return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
