#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import hashlib
import base64
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


# === Resolve Project Root ===
PROJECT_ROOT = find_project_root()

# Path to shared wordlist template
WORDLIST_TEMPLATE = PROJECT_ROOT / "flag_generators" / "wordlist.txt"


def md5_hash(password: str) -> str:
    """Return MD5 hash of a password."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def base64_encode(text: str) -> str:
    """Base64 encode the given text."""
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create hashes.txt, wordlist.txt, and password-protected ZIPs with encoded segments.
    """
    try:
        segments_dir = challenge_folder / "segments"
        segments_dir.mkdir(parents=True, exist_ok=True)

        # Check if wordlist template exists
        if not WORDLIST_TEMPLATE.exists():
            raise FileNotFoundError(
                f"❌ Wordlist template missing: {WORDLIST_TEMPLATE.relative_to(PROJECT_ROOT)}"
            )

        # Combine and split flags into parts
        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)

        part1 = [flag.split("-")[0] for flag in all_flags]
        part2 = [flag.split("-")[1] for flag in all_flags]
        part3 = [flag.split("-")[2] for flag in all_flags]

        # Write base64-encoded segment files
        encoded_files = []
        for idx, parts in enumerate([part1, part2, part3], start=1):
            encoded_text = "\n".join(parts)
            encoded_b64 = base64_encode(encoded_text)
            file_path = challenge_folder / f"encoded_segments{idx}.txt"
            file_path.write_text(encoded_b64)
            encoded_files.append(file_path)

        # Randomly pick 3 unique passwords from the wordlist
        all_passwords = WORDLIST_TEMPLATE.read_text().splitlines()
        if not all_passwords:
            raise ValueError("❌ Wordlist template is empty!")

        chosen_passwords = random.sample(all_passwords, 3)

        # Create hashes.txt and password-protected ZIPs
        hashes_txt = challenge_folder / "hashes.txt"
        hashes_txt.write_text("")  # Start fresh

        for idx, (password, file) in enumerate(zip(chosen_passwords, encoded_files), start=1):
            # Add MD5 hash to hashes.txt
            hash_line = md5_hash(password)
            hashes_txt.write_text(hashes_txt.read_text() + hash_line + "\n")

            # Zip and password protect
            zip_file = segments_dir / f"part{idx}.zip"
            result = subprocess.run(
                ["zip", "-P", password, str(zip_file), str(file)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"❌ Zip failed for {file.name}: {result.stderr.strip()}"
                )

            file.unlink()  # Remove plaintext encoded file

        # Copy shared wordlist.txt into challenge folder
        wordlist_file = challenge_folder / "wordlist.txt"
        wordlist_file.write_text("\n".join(all_passwords))

        print(
            f"🗝️ {hashes_txt.relative_to(PROJECT_ROOT)}, "
            f"{wordlist_file.relative_to(PROJECT_ROOT)}, "
            f"and 🔒 {segments_dir.relative_to(PROJECT_ROOT)} created "
            f"with random passwords: {', '.join(chosen_passwords)}"
        )

    except (FileNotFoundError, PermissionError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def generate_flag(challenge_folder: Path) -> str:
    """
    Generate real/fake flags and embed them into hashcat challenge assets.
    Returns the real flag in plaintext.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    print(f"✅ Admin flag: {real_flag}")
    return real_flag
