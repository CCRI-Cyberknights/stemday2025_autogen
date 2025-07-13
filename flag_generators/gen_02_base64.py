#!/usr/bin/env python3

import base64
import random
from pathlib import Path
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

GENERATOR_DIR = Path(__file__).parent

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create a memory_dump.txt in the challenge folder with base64-encoded flags.
    """
    memory_dump_file = challenge_folder / "memory_dump.txt"

    # Combine and shuffle flags
    all_flags = fake_flags + [real_flag]
    random.shuffle(all_flags)

    # Base64 encode each flag
    encoded_flags = [
        base64.b64encode(flag.encode("utf-8")).decode("utf-8")
        for flag in all_flags
    ]

    # Write to memory_dump.txt
    memory_dump_file.write_text(
        "Multiple values recovered from the memory dump. Only one is a valid CCRI flag.\n\n" +
        "\n".join(f"- {flag}" for flag in encoded_flags)
    )

    print(f"📄 memory_dump.txt created with {len(all_flags)} base64-encoded flags.")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate a real flag and fake flags, embed them into memory_dump.txt,
    and return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Make sure real flag isn’t duplicated accidentally
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
