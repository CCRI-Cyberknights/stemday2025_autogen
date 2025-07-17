#!/usr/bin/env python3

import random
import re
import sys
from pathlib import Path
from flag_generators.flag_helpers import FlagUtils


class NmapScanFlagGenerator:
    """
    Generator for the Nmap Scanning challenge.
    Dynamically patches web_version_admin/server.py with new ports and flags.
    """
    def __init__(self, project_root: Path = None, server_file: Path = None):
        self.project_root = project_root or self.find_project_root()
        self.server_file = server_file or self.project_root / "web_version_admin" / "server.py"

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

    def random_ports(self, port_range, count):
        """Pick unique random ports from a range"""
        return random.sample(port_range, count)

    def patch_server_file(self, real_flag: str, fake_flags: dict, real_port: int):
        """
        Update the FAKE_FLAGS block in server.py with the new ports and flags.
        """
        server_file = self.server_file.resolve()

        if not server_file.exists():
            print(f"❌ ERROR: {server_file} not found.", file=sys.stderr)
            sys.exit(1)

        try:
            # Build replacement FAKE_FLAGS block
            new_fake_flags = [f"    {real_port}: \"{real_flag}\",       # ✅ REAL FLAG"]
            for port, flag in fake_flags.items():
                new_fake_flags.append(f"    {port}: \"{flag}\",       # fake")
            new_fake_flags_block = "FAKE_FLAGS = {\n" + "\n".join(new_fake_flags) + "\n}"

            # Read server.py content
            print(f"📂 Reading {server_file}...")
            content = server_file.read_text(encoding="utf-8")

            # Replace FAKE_FLAGS block
            new_content, count = re.subn(
                r"FAKE_FLAGS\s*=\s*\{[^}]*\}",
                new_fake_flags_block,
                content,
                flags=re.DOTALL
            )

            if count == 0:
                raise RuntimeError("No FAKE_FLAGS block found to replace!")

            # Backup original server.py
            backup_file = server_file.with_suffix(".bak")
            server_file.replace(backup_file)
            print(f"🗄️ Backup created: {backup_file.name}")

            # Write updated server.py
            server_file.write_text(new_content, encoding="utf-8")
            print(f"✅ Updated {server_file.name}")

        except Exception as e:
            print(f"❌ ERROR during server.py patching: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate a real flag, update server.py with fake/real flags, and return real flag.
        """
        # Select random ports
        port_range = list(range(8000, 8100))
        selected_ports = self.random_ports(port_range, 5)
        real_port = selected_ports[0]
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = {port: FlagUtils.generate_fake_flag() for port in selected_ports[1:]}

        # Patch server.py with new flags
        self.patch_server_file(real_flag, fake_flags, real_port)

        # Return plaintext real flag
        print(f"🏁 Real flag: {real_flag} on port {real_port}")
        for port, flag in fake_flags.items():
            print(f"🎭 Fake flag: {flag} on port {port}")
        return real_flag
