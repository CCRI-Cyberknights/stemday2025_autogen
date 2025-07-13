#!/usr/bin/env python3
import os
import random
from pathlib import Path
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

def insert_flag(binary_data: bytearray, flag: str, offset: int):
    """
    Insert a flag string at a specific offset in the binary data.
    """
    flag_bytes = flag.encode("utf-8")
    binary_data[offset:offset + len(flag_bytes)] = flag_bytes

def generate_hex_flag_bin(output_path: Path):
    # Random binary size between 1KB and 1.5KB
    binary_size = random.randint(1024, 1536)
    binary_data = bytearray(os.urandom(binary_size))

    # Generate flags
    real_flag = generate_real_flag()
    fake_flags = []
    while len(fake_flags) < 4:
        fake = generate_fake_flag()
        if fake != real_flag and fake not in fake_flags:
            fake_flags.append(fake)

    # Pick random non-overlapping offsets
    max_offset = binary_size - max(len(real_flag), max(len(f) for f in fake_flags)) - 1
    offsets = random.sample(range(100, max_offset), 5)

    # Insert real flag
    insert_flag(binary_data, real_flag, offsets[0])

    # Insert fake flags
    for flag, offset in zip(fake_flags, offsets[1:]):
        insert_flag(binary_data, flag, offset)

    # Write binary file
    output_path.write_bytes(binary_data)
    print(f"✅ hex_flag.bin generated with:")
    print(f"   🏁 Real flag: {real_flag}")
    print(f"   🎭 Fake flags: {', '.join(fake_flags)}")
    print(f"📂 Saved to: {output_path}")

    return real_flag

if __name__ == "__main__":
    folder = Path(__file__).parent
    bin_file = folder / "hex_flag.bin"
    generate_hex_flag_bin(bin_file)
