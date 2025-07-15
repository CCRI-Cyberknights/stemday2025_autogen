#!/usr/bin/env python3
import random
import re
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

# === Resolve Paths ===
PROJECT_ROOT = find_project_root()
DEFAULT_SERVER_FILE = PROJECT_ROOT / "web_version_admin" / "server.py"


def random_ports(port_range, count):
    """Pick unique random ports from a range"""
    return random.sample(port_range, count)


def generate_flag(challenge_folder: Path, server_file: Path = DEFAULT_SERVER_FILE) -> str:
    """
    Update server.py with a new real flag and fake flags.
    Returns the real flag so it can be stored in challenges.json.
    """
    server_file = server_file.resolve()

    if not server_file.exists():
        print(f"❌ ERROR: {server_file} not found.", file=sys.stderr)
        sys.exit(1)

    try:
        # Pick ports and flags
        port_range = list(range(8000, 8100))
        selected_ports = random_ports(port_range, 5)
        real_port = selected_ports[0]
        real_flag = generate_real_flag()
        fake_ports = selected_ports[1:]
        fake_flags = {port: generate_fake_flag() for port in fake_ports}

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
            print("⚠️ WARNING: No FAKE_FLAGS block found to replace!", file=sys.stderr)
            sys.exit(1)

        # Backup original file
        backup_file = server_file.with_suffix(".bak")
        server_file.replace(backup_file)
        print(f"🗄️ Backup created: {backup_file}")

        # Write updated content
        server_file.write_text(new_content, encoding="utf-8")
        print(f"✅ Updated {server_file}")

        # Show summary
        print(f"🏁 Real flag: {real_flag} on port {real_port}")
        for port, flag in fake_flags.items():
            print(f"🎭 Fake flag: {flag} on port {port}")

        return real_flag

    except Exception as e:
        print(f"❌ ERROR during server.py update: {e}", file=sys.stderr)
        sys.exit(1)
