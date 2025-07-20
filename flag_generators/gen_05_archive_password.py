#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import base64
import sys
from flag_generators.flag_helpers import FlagUtils


class ArchivePasswordFlagGenerator:
    """
    Generator for the Archive Password challenge.
    Embeds real and fake flags into a password-protected ZIP archive.
    """
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()
        self.wordlist_template = self.project_root / "flag_generators" / "wordlist.txt"

    @staticmethod
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

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Create wordlist.txt and password-protected secret.zip containing message_encoded.txt.
        """
        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            if not self.wordlist_template.exists():
                raise FileNotFoundError(
                    f"❌ Wordlist template missing: {self.wordlist_template.relative_to(self.project_root)}"
                )

            # Load master wordlist
            all_passwords = self.wordlist_template.read_text().splitlines()
            if not all_passwords:
                raise ValueError("❌ Wordlist template is empty!")

            # Randomly pick a password
            correct_password = random.choice(all_passwords)

            # Copy wordlist.txt into challenge folder
            wordlist_file = challenge_folder / "wordlist.txt"
            wordlist_file.write_text("\n".join(all_passwords))

            # Create message_encoded.txt (base64-encoded flags)
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)
            message = (
                "Mission Debrief:\n\n"
                "Encrypted transmission recovered from target machine.\n"
                "Analysis reveals five potential keys, but only one fits agency format.\n\n"
                "Decoded entries:\n" +
                "\n".join(f"- {flag}" for flag in all_flags) +
                "\n\nProceed with caution."
            )
            message_encoded = base64.b64encode(message.encode("utf-8")).decode("utf-8")

            encoded_file = challenge_folder / "message_encoded.txt"
            encoded_file.write_text(message_encoded)

            # Create password-protected ZIP
            zip_file = challenge_folder / "secret.zip"
            result = subprocess.run(
                ["zip", "-P", correct_password, str(zip_file), str(encoded_file)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"❌ Zip failed: {result.stderr.strip()}")

            # Clean up temp file
            encoded_file.unlink()
            print(f"🗝️ {wordlist_file.relative_to(self.project_root)} and 🔒 {zip_file.relative_to(self.project_root)} created with correct password: {correct_password}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate and embed real/fake flags for the Archive Password challenge.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
