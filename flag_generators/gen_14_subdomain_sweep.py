#!/usr/bin/env python3

from pathlib import Path
import random
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

SUBDOMAINS = [
    ("alpha.liber8.local", "Alpha Service Portal", "Alpha Service", "Welcome to the Alpha team portal. All systems operational."),
    ("beta.liber8.local", "Beta Operations Dashboard", "Beta Operations", "Restricted Access – Authorized Personnel Only"),
    ("gamma.liber8.local", "Gamma Data API", "Gamma Data API", "Status: Maintenance Mode"),
    ("delta.liber8.local", "Delta API Service", "Delta API", "REST API Portal for Internal Use Only"),
    ("omega.liber8.local", "Omega Internal Tools", "Omega Tools Suite", "For Internal Testing and Deployment")
]

FOOTERS = [
    "Alpha Service © 2025 Liber8 Network",
    "Beta Dashboard – Liber8 Internal Systems",
    "© 2025 Liber8 Network – Gamma Team",
    "Delta Service © Liber8 DevOps",
    "Omega Tools © Liber8 Engineering"
]

ALT_DESCRIPTIONS = [
    "System running in nominal state.",
    "All services operational.",
    "Internal use only. Contact admin for access.",
    "REST API endpoints active and monitored.",
    "Scheduled maintenance ongoing. Expect delays."
]

ALT_PRE_LINES = [
    "[INFO] Service heartbeat received.",
    "[DEBUG] Connection pool warmed up.",
    "[TRACE] User session started: {}",
    "[WARN] Unexpected response code: 503",
    "[INFO] Scheduled job completed successfully.",
    "[DEBUG] Cache cleared for /api/v1/resources.",
    "[NOTICE] Authentication handshake completed."
]

def generate_logs(flag: str) -> str:
    """
    Generate 3-5 log lines, embedding the flag in one randomly.
    """
    lines = random.sample(ALT_PRE_LINES, random.randint(3, 5))
    insert_pos = random.randint(0, len(lines) - 1)
    lines[insert_pos] = lines[insert_pos].format(flag)
    return "\n".join(lines)

def embed_flag(flag: str) -> str:
    """
    Randomly embed the flag in either a <p> or <pre> block (both visible in browser).
    """
    if random.random() < 0.5:
        # Place in a <p> block
        return f"<p><strong>Note:</strong> {flag}</p>"
    else:
        # Place in a <pre> block
        return f"<pre>\n{generate_logs(flag)}\n</pre>"

def create_html(subdomain: str, title: str, header_title: str, header_desc: str, footer: str, flag: str) -> str:
    """
    Generate randomized HTML content for a subdomain.
    """
    alt_desc = random.choice(ALT_DESCRIPTIONS) if random.random() < 0.4 else header_desc
    flag_block = embed_flag(flag)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
</head>
<body>
  <header>
    <h1>{header_title}</h1>
    <p>{alt_desc}</p>
  </header>

  <main>
    <section>
      <h2>Recent Activity</h2>
      {flag_block}
    </section>

    <section>
      <h2>Status</h2>
      <p>{alt_desc}</p>
    </section>
  </main>

  <footer>
    <p>{footer}</p>
  </footer>
</body>
</html>"""

def embed_subdomain_html(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Generate HTML files for each subdomain.
    """
    flags = fake_flags + [real_flag]
    random.shuffle(flags)

    for (subdomain, title, header_title, header_desc), footer, flag in zip(SUBDOMAINS, FOOTERS, flags):
        file_path = challenge_folder / f"{subdomain}.html"
        html_content = create_html(subdomain, title, header_title, header_desc, footer, flag)
        file_path.write_text(html_content)

        if flag == real_flag:
            print(f"✅ {file_path.name} (REAL flag)")
        else:
            print(f"➖ {file_path.name} (decoy)")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate subdomain HTML files with 1 real and 4 fake flags.
    Return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = list({generate_fake_flag() for _ in range(4)})

    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_subdomain_html(challenge_folder, real_flag, fake_flags)
    return real_flag
