#!/usr/bin/env python3

from pathlib import Path
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

# === Resolve Project Root ===
PROJECT_ROOT = find_project_root()

# === Predefined header and body variants ===
SERVERS = [
    "Liber8-Server/2.3.1",
    "Liber8-Server/3.0.0-beta",
    "Apache/2.4.54 (Ubuntu)",
    "nginx/1.24.0",
    "Go HTTP Server/1.19"
]

POWERED_BY = [
    "PHP/8.1.12",
    "Python/3.11.4",
    "Node.js/18.16.0",
    "ASP.NET Core/7.0",
    "Ruby on Rails/7.1.0"
]

CONTENT_TYPES = [
    "text/html; charset=UTF-8",
    "application/json",
    "text/plain; charset=UTF-8",
]

CACHE_CONTROLS = [
    "no-store",
    "public, max-age=86400",
    "private, no-cache"
]

HTML_BODIES = [
    """<html>
  <head><title>Liber8 Portal</title></head>
  <body>
    <h1>Welcome to Liber8</h1>
    <p>System maintenance is underway. Some services may be unavailable.</p>
  </body>
</html>""",
    """<html>
  <head><title>Internal Dashboard</title></head>
  <body>
    <h1>Liber8 Ops Dashboard</h1>
    <p>Authentication successful. Redirecting...</p>
  </body>
</html>""",
    """<html>
  <head><title>Data Service</title></head>
  <body>
    <h1>Data Service Ready</h1>
    <p>Connect your client application to begin.</p>
  </body>
</html>""",
    """{
  "status": "ok",
  "message": "API version 1.2.4 is running.",
  "notes": "No maintenance scheduled."
}""",
    """Welcome to the Liber8 data endpoint.
This endpoint returns plain text responses."""
]

HTML_COMMENTS = [
    "<!-- Debug: Temporary caching enabled -->",
    "<!-- Developer note: Remove X-Test headers before release -->",
    "<!-- Debug: API response size 512 bytes -->",
    "<!-- Debug: Session created for client 10.6.112.3 -->",
    "<!-- To-do: Update security headers on staging -->"
]

def generate_http_response(flag: str) -> str:
    """
    Generate a realistic HTTP response string with flag in X-Flag header.
    """
    headers = [
        "HTTP/1.1 200 OK",
        f"Date: Sun, 30 Jun 2025 15:{random.randint(45, 59)}:{random.randint(0,59):02} GMT",
        f"Server: {random.choice(SERVERS)}",
        f"Content-Type: {random.choice(CONTENT_TYPES)}",
        f"Cache-Control: {random.choice(CACHE_CONTROLS)}",
        f"X-Powered-By: {random.choice(POWERED_BY)}",
        f"X-Flag: {flag}",
        "X-Frame-Options: SAMEORIGIN",
        "X-Content-Type-Options: nosniff"
    ]

    # Optionally add Set-Cookie for realism
    if random.random() < 0.6:
        session_id = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12))
        headers.append(f"Set-Cookie: sessionid={session_id}; HttpOnly; Secure")

    random.shuffle(headers[5:])  # Shuffle optional headers

    body = random.choice(HTML_BODIES)
    comment = random.choice(HTML_COMMENTS)

    return "\n".join(headers) + "\n\n" + body + "\n\n" + comment

def clean_old_responses(challenge_folder: Path):
    """
    Remove old response_*.txt files from challenge folder.
    """
    for old_file in challenge_folder.glob("response_*.txt"):
        try:
            old_file.unlink()
            print(f"🗑️ Removed old file: {old_file.name}")
        except Exception as e:
            print(f"⚠️ Could not delete {old_file.name}: {e}", file=sys.stderr)

def embed_http_responses(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Generate 5 response files with headers, one containing the real flag.
    """
    try:
        challenge_folder.mkdir(parents=True, exist_ok=True)
        clean_old_responses(challenge_folder)

        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)

        for i, flag in enumerate(all_flags, start=1):
            file_path = challenge_folder / f"response_{i}.txt"
            response_content = generate_http_response(flag)
            file_path.write_text(response_content)

            if flag == real_flag:
                print(f"✅ {file_path.name} (REAL flag)")
            else:
                print(f"➖ {file_path.name} (decoy)")
    except Exception as e:
        print(f"❌ Failed during HTTP response embedding: {e}", file=sys.stderr)
        sys.exit(1)

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate HTTP response files with 1 real and 4 fake flags.
    Return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = list({generate_fake_flag() for _ in range(4)})

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_http_responses(challenge_folder, real_flag, fake_flags)
    return real_flag
