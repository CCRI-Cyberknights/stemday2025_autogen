#!/usr/bin/env python3

import base64
import random
import sys
from pathlib import Path
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
GENERATOR_DIR = PROJECT_ROOT / "flag_generators"

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Create a memory_dump.txt in the challenge folder with base64-encoded flags.
    """
    memory_dump_file = challenge_folder / "memory_dump.txt"

    try:
        # Sanity check: ensure challenge folder exists
        if not challenge_folder.exists():
            raise FileNotFoundError(f"❌ Challenge folder not found: {challenge_folder.relative_to(PROJECT_ROOT)}")

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

    except PermissionError:
        print(f"❌ Permission denied: Cannot write to {memory_dump_file.relative_to(PROJECT_ROOT)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate a real flag and fake flags, embed them into memory_dump.txt,
    and return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure real flag isn’t duplicated accidentally
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
