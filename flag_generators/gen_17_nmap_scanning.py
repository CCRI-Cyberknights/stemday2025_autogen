#!/usr/bin/env python3
import random
import string
import re

SERVER_FILE = "stemday2025/web_version_admin/server.py"

def random_flag(prefix="CCRI"):
    """Generate a flag in CCRI-XXXX-1234 format"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = random.randint(1000, 9999)
    return f"{prefix}-{letters}-{digits}"

def random_ports(port_range, count):
    """Pick unique random ports"""
    return random.sample(port_range, count)

# --- Generate random ports and flags ---
port_range = list(range(8000, 8100))
selected_ports = random_ports(port_range, 5)

real_port = selected_ports[0]
real_flag = random_flag()  # Real flag
fake_ports = selected_ports[1:]
fake_flags = {port: random_flag("FAKE") for port in fake_ports}

# Build FAKE_FLAGS replacement
new_fake_flags = [f"    {real_port}: \"{real_flag}\",       # ✅ REAL FLAG"]
for port, flag in fake_flags.items():
    new_fake_flags.append(f"    {port}: \"{flag}\",       # fake")

# Assemble new block
new_fake_flags_block = "FAKE_FLAGS = {\n" + "\n".join(new_fake_flags) + "\n}"

# --- Update server.py ---
with open(SERVER_FILE, "r", encoding="utf-8") as f:
    server_py = f.read()

# Replace FAKE_FLAGS block only
server_py = re.sub(
    r"FAKE_FLAGS\s*=\s*\{[^}]*\}",
    new_fake_flags_block,
    server_py,
    flags=re.DOTALL
)

# Write back changes
with open(SERVER_FILE, "w", encoding="utf-8") as f:
    f.write(server_py)

print(f"🎉 Updated {SERVER_FILE}:")
print(f"✅ Real flag: {real_flag} on port {real_port}")
for port, flag in fake_flags.items():
    print(f"🎭 Fake flag: {flag} on port {port}")
