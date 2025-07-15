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

# Sample users, commands, and args
USERS = ["root", "user1", "user2", "user3", "daemon", "syslog", "mysql", "postfix", "nobody", "liber8"]
COMMANDS = [
    "/usr/sbin/apache2 -k start",
    "/usr/bin/nano /home/user{}/notes.txt",
    "/usr/bin/python3 /usr/lib/update-manager/check-new-release",
    "/usr/bin/firefox --no-remote",
    "/usr/bin/gedit /home/user{}/todo.txt",
    "/usr/bin/vlc /home/user{}/video.mp4",
    "/usr/sbin/ufw --daemon",
    "/usr/sbin/rsyslogd -n",
    "/usr/bin/thunderbird",
    "/usr/sbin/sshd -D",
    "/usr/sbin/acpid",
    "/usr/bin/htop",
    "/usr/bin/code /home/user{}/project",
    "/lib/systemd/systemd-journald",
    "/usr/sbin/cron -f",
    "/usr/sbin/irqbalance",
    "/usr/local/bin/tunneler --mode passive --ttl 128",
    "/usr/bin/harvest --scan --output /tmp/result.log",
    "/opt/liber8/bin/siphon --threads 8 --proxy 127.0.0.1:8080"
]

def random_stat():
    return random.choice(["S", "Ss", "Sl", "Ssl", "R", "R+", "Z", "D"])

def random_start_time():
    return f"Jul{random.randint(1, 30):02d}"

def random_process(user_override=None, cmd_override=None):
    """
    Generate a single ps-like process line.
    """
    user = user_override or random.choice(USERS)
    pid = random.randint(100, 9999)
    cpu = round(random.uniform(0.1, 1.5), 1)
    mem = round(random.uniform(0.1, 1.5), 1)
    vsz = random.randint(15000, 80000)
    rss = random.randint(3000, 40000)
    tty = random.choice(["?", "pts/0", "pts/1"])
    stat = random_stat()
    start = random_start_time()
    time = f"{random.randint(0, 2)}:{random.randint(0, 59):02d}"
    cmd_template = cmd_override or random.choice(COMMANDS)
    cmd = cmd_template.format(random.randint(1, 3))

    return f"{user:<10}{pid:<6}{cpu:<5}{mem:<5}{vsz:<8}{rss:<7}{tty:<10}{stat:<5}{start:<8}{time:<7}{cmd}"

def embed_flags(lines, real_flag, fake_flags):
    """
    Embed 1 real and several fake flags in process commands.
    """
    flag_processes = [
        "/usr/bin/harvest --target 10.6.42.18 --flag={} --interval 15 --verbose",
        "/opt/liber8/bin/siphon --upload --flag={} --threads 4",
        "/usr/local/bin/tunneler --flag={} --mode aggressive --ttl 64",
        "/usr/bin/stealth --flag={} --timeout 90",
        "/usr/sbin/backdoor --flag={} --listen --port 4444"
    ]

    # Shuffle flags and embed
    flags = [real_flag] + fake_flags
    random.shuffle(flag_processes)
    for proc, flag in zip(flag_processes, flags):
        lines.append(random_process("liber8", proc.format(flag)))

def generate_ps_dump(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Generate ps_dump.txt file with fake and real processes.
    """
    challenge_folder.mkdir(parents=True, exist_ok=True)
    dump_file = challenge_folder / "ps_dump.txt"

    try:
        lines = ["USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"]
        # Add random background noise
        for _ in range(random.randint(80, 100)):
            lines.append(random_process())

        # Embed flagged processes
        embed_flags(lines, real_flag, fake_flags)

        # Shuffle all except header line
        random.shuffle(lines[1:])

        # Write output
        dump_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"✅ ps_dump.txt created in {challenge_folder} (real flag: {real_flag})")

    except Exception as e:
        print(f"❌ Error writing ps_dump.txt: {e}", file=sys.stderr)
        sys.exit(1)

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate the challenge with real/fake flags embedded in ps_dump.txt.
    """
    real_flag = generate_real_flag()
    fake_flags = list({generate_fake_flag() for _ in range(4)})

    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    generate_ps_dump(challenge_folder, real_flag, fake_flags)
    return real_flag
