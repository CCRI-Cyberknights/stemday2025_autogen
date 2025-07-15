#!/usr/bin/env python3
import os
import random
import sys
from pathlib import Path
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

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

def insert_flag(binary_data: bytearray, flag: str, offset: int):
    """
    Insert a flag string at a specific offset in the binary data.
    """
    flag_bytes = flag.encode("utf-8")
    if offset + len(flag_bytes) > len(binary_data):
        raise ValueError(f"❌ Offset {offset} + flag length {len(flag_bytes)} exceeds binary size {len(binary_data)}")
    binary_data[offset:offset + len(flag_bytes)] = flag_bytes

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate hex_flag.bin in the challenge folder with 1 real flag and 4 fake flags.
    Returns the real flag for challenges.json.
    """
    try:
        # Ensure challenge folder is absolute and relative to project root
        full_folder = (PROJECT_ROOT / challenge_folder).resolve()
        full_folder.mkdir(parents=True, exist_ok=True)

        binary_size = random.randint(1024, 1536)
        binary_data = bytearray(os.urandom(binary_size))

        # Generate flags
        real_flag = generate_real_flag()
        fake_flags = []
        while len(fake_flags) < 4:
            fake = generate_fake_flag()
            if fake != real_flag and fake not in fake_flags:
                fake_flags.append(fake)

        # Ensure binary is large enough for flag embedding
        longest_flag_len = max(len(real_flag), max(len(f) for f in fake_flags))
        if binary_size < longest_flag_len + 200:
            raise RuntimeError("❌ Binary size too small for safe flag embedding.")

        # Pick random non-overlapping offsets
        max_offset = binary_size - longest_flag_len - 1
        offsets = random.sample(range(100, max_offset), 5)

        # Insert real flag
        insert_flag(binary_data, real_flag, offsets[0])

        # Insert fake flags
        for flag, offset in zip(fake_flags, offsets[1:]):
            insert_flag(binary_data, flag, offset)

        # Write binary file
        output_path = full_folder / "hex_flag.bin"
        output_path.write_bytes(binary_data)

        print(f"✅ hex_flag.bin generated in {full_folder}")
        print(f"   🏁 Real flag: {real_flag}")
        print(f"   🎭 Fake flags: {', '.join(fake_flags)}")
        return real_flag  # ✅ Needed for challenges.json update

    except Exception as e:
        print(f"❌ Error during hex_flag.bin generation: {e}", file=sys.stderr)
        sys.exit(1)
