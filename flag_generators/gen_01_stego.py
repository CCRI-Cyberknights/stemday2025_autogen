#!/usr/bin/env python3

from pathlib import Path
import subprocess
import random
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

# === Resolve Paths ===
PROJECT_ROOT = find_project_root()
GENERATOR_DIR = PROJECT_ROOT / "flag_generators"
SOURCE_IMAGE = GENERATOR_DIR / "squirrel.jpg"

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list, passphrase="password"):
    """
    Copy pristine squirrel.jpg into the challenge folder and embed real + fake flags.
    """
    dest_image = challenge_folder / "squirrel.jpg"
    hidden_file = challenge_folder / "hidden_flags.txt"

    try:
        # Sanity check
        if not SOURCE_IMAGE.exists():
            raise FileNotFoundError(f"❌ Source image not found: {SOURCE_IMAGE.relative_to(PROJECT_ROOT)}")

        # Copy clean squirrel.jpg into challenge folder
        dest_image.write_bytes(SOURCE_IMAGE.read_bytes())
        print(f"📂 Copied {SOURCE_IMAGE.name} to {challenge_folder.relative_to(PROJECT_ROOT)}")

        # Combine and shuffle flags
        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)
        hidden_file.write_text("\n".join(all_flags))
        print(f"📝 Hidden flags saved to temporary file: {hidden_file.name}")

        # Embed flags with steghide
        print(f"🛠️ Embedding flags into {dest_image.name} using steghide...")
        subprocess.run([
            "steghide", "embed",
            "-cf", str(dest_image),
            "-ef", str(hidden_file),
            "-p", passphrase
        ], check=True)
        print(f"✅ Steghide embedding complete for {challenge_folder.name}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        sys.exit(1)
    except subprocess.CalledProcessError as steghide_error:
        print(f"❌ Steghide failed with error: {steghide_error}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Cleanup temp file
        if hidden_file.exists():
            try:
                hidden_file.unlink()
                print(f"🗑️ Cleaned up temporary file: {hidden_file.name}")
            except Exception as cleanup_error:
                print(f"⚠️ Failed to delete {hidden_file.name}: {cleanup_error}")

def generate_flag(challenge_folder: Path) -> str:
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}
    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
