#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

def check_qrencode_installed():
    """Verify qrencode is installed, or exit with error."""
    result = subprocess.run(["which", "qrencode"], capture_output=True)
    if result.returncode != 0:
        print("❌ qrencode is not installed. Please run: sudo apt install qrencode")
        exit(1)

def create_qr_code(output_file: Path, text: str):
    """Use qrencode to generate a QR code PNG."""
    subprocess.run(["qrencode", "-o", str(output_file), text], check=True)

def embed_flags_as_qr(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Generate 5 QR codes in the challenge folder: 1 real flag and 4 fake flags.
    """
    # Combine and shuffle flags
    all_flags = fake_flags + [real_flag]
    random.shuffle(all_flags)

    print("🎯 Generating QR codes in:", challenge_folder)
    for i, flag in enumerate(all_flags, start=1):
        qr_file = challenge_folder / f"qr_{i:02}.png"
        create_qr_code(qr_file, flag)
        if flag == real_flag:
            print(f"✅ {qr_file.name} (REAL flag)")
        else:
            print(f"➖ {qr_file.name} (decoy)")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate QR code PNGs with 1 real and 4 fake flags.
    Return the real flag.
    """
    check_qrencode_installed()

    real_flag = generate_real_flag()
    fake_flags = list({generate_fake_flag() for _ in range(4)})

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags_as_qr(challenge_folder, real_flag, fake_flags)
    return real_flag
