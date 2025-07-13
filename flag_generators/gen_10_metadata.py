#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
from flag_helpers import generate_real_flag, generate_fake_flag

GENERATOR_DIR = Path(__file__).parent

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Copy pristine capybara.jpg into the challenge folder and embed real + fake flags in EXIF metadata.
    """
    source_image = GENERATOR_DIR / "capybara.jpg"
    dest_image = challenge_folder / "capybara.jpg"

    # Copy clean capybara.jpg into challenge folder
    dest_image.write_bytes(source_image.read_bytes())

    # Assign flags to metadata fields
    random.shuffle(fake_flags)
    metadata_tags = {
        "ImageDescription": fake_flags[0],
        "Artist": fake_flags[1],
        "Copyright": fake_flags[2],
        "XPKeywords": fake_flags[3],
        "UserComment": real_flag  # Embed the real flag here
    }

    print(f"📝 Embedding flags into metadata...")
    for tag, value in metadata_tags.items():
        subprocess.run(
            ["exiftool", f"-{tag}={value}", str(dest_image)],
            check=True,
            stdout=subprocess.DEVNULL
        )

    # Remove backup file exiftool creates (capybara.jpg_original)
    backup_file = dest_image.with_suffix(dest_image.suffix + "_original")
    if backup_file.exists():
        backup_file.unlink()

    print(f"✅ Embedded real flag in UserComment: {real_flag}")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate real and fake flags, embed them into capybara.jpg metadata,
    and return the real flag.
    """
    real_flag = generate_real_flag(prefix="CCRI-META")
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag(prefix="CCRI-META")

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
