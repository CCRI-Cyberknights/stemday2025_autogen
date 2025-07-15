#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import sys
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

GENERATOR_DIR = Path(__file__).parent

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Copy pristine capybara.jpg into the challenge folder and embed real + fake flags in EXIF metadata.
    """
    source_image = GENERATOR_DIR / "capybara.jpg"
    dest_image = challenge_folder / "capybara.jpg"

    # === Check if exiftool is installed ===
    if not shutil.which("exiftool"):
        print("❌ exiftool is not installed. Please install it first.")
        sys.exit(1)

    # === Copy clean capybara.jpg into challenge folder ===
    try:
        dest_image.write_bytes(source_image.read_bytes())
    except FileNotFoundError:
        print(f"❌ Source image not found: {source_image}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to copy image: {e}")
        sys.exit(1)

    # === Assign flags to metadata fields ===
    random.shuffle(fake_flags)
    metadata_tags = {
        "ImageDescription": fake_flags[0],
        "Artist": fake_flags[1],
        "Copyright": fake_flags[2],
        "XPKeywords": fake_flags[3],
        "UserComment": real_flag  # Embed the real flag here
    }

    print("📝 Embedding flags into EXIF metadata...")
    try:
        for tag, value in metadata_tags.items():
            result = subprocess.run(
                ["exiftool", f"-{tag}={value}", str(dest_image)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
    except subprocess.CalledProcessError as e:
        print(f"❌ exiftool failed: {e.stderr.strip()}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error while embedding metadata: {e}")
        sys.exit(1)

    # === Remove exiftool backup file (capybara.jpg_original) ===
    backup_file = dest_image.with_suffix(dest_image.suffix + "_original")
    if backup_file.exists():
        try:
            backup_file.unlink()
            print("🗑️ Cleaned up exiftool backup file.")
        except Exception as e:
            print(f"⚠️ Could not remove backup file: {e}")

    print(f"✅ Embedded real flag in UserComment: {real_flag}")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate real and fake flags, embed them into capybara.jpg metadata,
    and return the real flag.
    """
    # Manually add "META" to the prefix
    real_flag = generate_real_flag().replace("CCRI-", "CCRI-META-")

    # Generate unique fake flags
    fake_flags = set()
    while len(fake_flags) < 4:
        fake = generate_fake_flag().replace("CCRI-", "FAKE-")
        fake_flags.add(fake)

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
