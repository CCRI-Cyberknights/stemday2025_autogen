#!/usr/bin/env python3
import random
import re
from pathlib import Path
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

# Default server.py path for admin bundle
DEFAULT_SERVER_FILE = Path(__file__).parent.parent / "web_version_admin" / "server.py"

def random_ports(port_range, count):
    """Pick unique random ports"""
    return random.sample(port_range, count)

def generate_flag(challenge_folder: Path, server_file: Path = DEFAULT_SERVER_FILE) -> str:
    """
    Update server.py with a new real flag and fake flags.
    Returns the real flag so it can be stored in challenges.json.
    """
    port_range = list(range(8000, 8100))
    selected_ports = random_ports(port_range, 5)

    real_port = selected_ports[0]
    real_flag = generate_real_flag()  # ✅ Generate real CCRI flag
    fake_ports = selected_ports[1:]
    fake_flags = {port: generate_fake_flag() for port in fake_ports}

    # Build FAKE_FLAGS replacement
    new_fake_flags = [f"    {real_port}: \"{real_flag}\",       # ✅ REAL FLAG"]
    for port, flag in fake_flags.items():
        new_fake_flags.append(f"    {port}: \"{flag}\",       # fake")

    new_fake_flags_block = "FAKE_FLAGS = {\n" + "\n".join(new_fake_flags) + "\n}"

    # --- Update server.py ---
    print(f"🔄 Updating {server_file}...")
    with open(server_file, "r", encoding="utf-8") as f:
        server_py = f.read()

    # Replace FAKE_FLAGS block only
    server_py = re.sub(
        r"FAKE_FLAGS\s*=\s*\{[^}]*\}",
        new_fake_flags_block,
        server_py,
        flags=re.DOTALL
    )

    # Write back changes
    with open(server_file, "w", encoding="utf-8") as f:
        f.write(server_py)

    print(f"🎉 Updated {server_file}:")
    print(f"✅ Real flag: {real_flag} on port {real_port}")
    for port, flag in fake_flags.items():
        print(f"🎭 Fake flag: {flag} on port {port}")

    return real_flag  # ✅ Return so challenges.json gets updated
