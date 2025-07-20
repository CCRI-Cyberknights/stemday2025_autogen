#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import sys
from flag_generators.flag_helpers import FlagUtils


class QRCodeFlagGenerator:
    """
    Generator for the QR Codes challenge.
    Produces 5 QR code PNGs in the challenge folder with 1 real flag and 4 decoys.
    """

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()

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

    @staticmethod
    def check_qrencode_installed():
        """Verify qrencode is installed, or exit with error."""
        result = subprocess.run(["which", "qrencode"], capture_output=True)
        if result.returncode != 0:
            print("❌ ERROR: qrencode is not installed.")
            print("👉 To fix, run: sudo apt install qrencode")
            sys.exit(1)
        else:
            print("✅ qrencode is installed.")

    def create_qr_code(self, output_file: Path, text: str):
        """Use qrencode to generate a QR code PNG."""
        try:
            subprocess.run(["qrencode", "-o", str(output_file), text], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate QR code: {e}", file=sys.stderr)
            sys.exit(1)

    def clean_qr_codes(self, folder: Path):
        """Remove any old QR codes in the challenge folder."""
        try:
            for qr_file in folder.glob("qr_*.png"):
                qr_file.unlink()
                print(f"🗑️ Removed old file: {qr_file.name}")
        except Exception as e:
            print(f"⚠️ Could not delete QR code(s) in {folder.relative_to(self.project_root)}: {e}", file=sys.stderr)

    def embed_flags_as_qr(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Generate 5 QR codes in the challenge folder: 1 real flag and 4 fake flags.
        """
        self.clean_qr_codes(challenge_folder)

        # Combine and shuffle flags
        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)

        print(f"🎭 Fake flags: {', '.join(fake_flags)}")  # <-- Added printout of fake flags

        print(f"🎯 Generating QR codes in: {challenge_folder.relative_to(self.project_root)}")
        for i, flag in enumerate(all_flags, start=1):
            qr_file = challenge_folder / f"qr_{i:02}.png"
            self.create_qr_code(qr_file, flag)
            if flag == real_flag:
                print(f"✅ {qr_file.name} (REAL flag)")
            else:
                print(f"➖ {qr_file.name} (decoy)")

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate QR code PNGs with 1 real and 4 fake flags.
        Return the real flag.
        """
        self.check_qrencode_installed()

        real_flag = FlagUtils.generate_real_flag()
        fake_flags = list({FlagUtils.generate_fake_flag() for _ in range(4)})

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags_as_qr(challenge_folder, real_flag, fake_flags)
        return real_flag
