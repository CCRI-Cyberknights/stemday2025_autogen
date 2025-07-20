#!/usr/bin/env python3

from pathlib import Path
import base64
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class Base64FlagGenerator:
    """
    Generator for the Base64 intercepted message challenge.
    Encodes an intercepted transmission (including flags) into encoded.txt.
    """
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()

        # === Exported unlock data for validation ===
        self.last_fake_flags = []

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
        Create encoded.txt in the challenge folder with base64-encoded intercepted message.
        """
        encoded_file = challenge_folder / "encoded.txt"

        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            # Combine and shuffle flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            # Build plaintext intercepted message
            message = (
                "Transmission Start\n"
                "------------------------\n"
                "To: LIBER8 Command Node\n"
                "From: Field Agent 4\n\n"
                "Flag candidates identified during network sweep. "
                "Message encoded for secure transit.\n\n"
                "Candidates:\n"
                + "\n".join(f"- {flag}" for flag in all_flags)
                + "\n\nVerify and submit the authentic CCRI flag.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            # Base64 encode the entire message
            encoded_message = base64.b64encode(message.encode("utf-8")).decode("utf-8")

            # Write to encoded.txt
            encoded_file.write_text(
                encoded_message + "\n"
            )
            print(f"📄 {encoded_file.relative_to(self.project_root)} created with Base64-encoded transmission.")

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {encoded_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate flags and embed them into encoded.txt.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        # Ensure real flag isn’t duplicated accidentally
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.last_fake_flags = fake_flags  # Store for validation

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
