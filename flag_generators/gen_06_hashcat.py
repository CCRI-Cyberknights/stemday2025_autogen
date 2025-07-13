#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import hashlib
import base64
from flag_helpers import generate_real_flag, generate_fake_flag

# Path to shared wordlist
WORDLIST_TEMPLATE = Path(__file__).parent / "wordlist.txt"

def md5_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def base64_encode(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create hashes.txt, wordlist.txt, and password-protected ZIPs with encoded segments.
    """
    segments_dir = challenge_folder / "segments"
    segments_dir.mkdir(parents=True, exist_ok=True)

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
        filename = f"encoded_segments{idx}.txt"
        file_path = challenge_folder / filename
        file_path.write_text(encoded_b64)
        encoded_files.append(file_path)

    # Randomly pick 3 unique passwords from the wordlist
    all_passwords = WORDLIST_TEMPLATE.read_text().splitlines()
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
        subprocess.run([
            "zip", "-P", password, str(zip_file), str(file)
        ], check=True)

        file.unlink()  # Remove plaintext encoded file

    # Copy shared wordlist.txt into challenge folder
    wordlist_file = challenge_folder / "wordlist.txt"
    wordlist_file.write_text("\n".join(all_passwords))

    print(f"🗝️ hashes.txt, wordlist.txt, and 🔒 segments created with random passwords: {', '.join(chosen_passwords)}")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate real/fake flags and embed them into hashcat challenge.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
