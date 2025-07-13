#!/usr/bin/env python3

from pathlib import Path
import subprocess
from flag_helpers import generate_real_flag, generate_fake_flag

GENERATOR_DIR = Path(__file__).parent

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list, passphrase="student"):
    """
    Copy pristine squirrel.jpg into the challenge folder and embed real + fake flags.
    """
    source_image = GENERATOR_DIR / "squirrel.jpg"
    dest_image = challenge_folder / "squirrel.jpg"
    hidden_file = challenge_folder / "hidden_flags.txt"

    # Copy clean squirrel.jpg into challenge folder
    dest_image.write_bytes(source_image.read_bytes())

    # Combine and shuffle flags
    all_flags = fake_flags + [real_flag]
    random.shuffle(all_flags)
    hidden_file.write_text("\n".join(all_flags))

    print(f"📂 Embedding {len(all_flags)} flags into {dest_image.name}...")

    subprocess.run([
        "steghide", "embed",
        "-cf", str(dest_image),
        "-ef", str(hidden_file),
        "-p", passphrase
    ], check=True)

    hidden_file.unlink()
    print(f"✅ Steghide embedding complete for {challenge_folder.name}.")

def generate_flag(challenge_folder: Path) -> str:
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}
    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
