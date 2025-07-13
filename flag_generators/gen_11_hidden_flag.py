#!/usr/bin/env python3

from pathlib import Path
import random
import shutil
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

# Fixed folder layout
FOLDERS_AND_FILES = {
    "backup": ["sysdump.bak", ".config.old"],
    "data": ["info.tmp", ".hint_file", ".summary"],
    "logs": ["old.log", ".keep.tmp", ".notes"],
    "ref": ["readme.txt", ".archive"],
}

# Exact file name → junk text snippets
FILE_BASED_JUNK = {
    "sysdump.bak": [
        "### System Memory Dump ###",
        "Heap analysis: no anomalies detected.",
        "Saved core dump for developer inspection.",
    ],
    ".config.old": [
        "# Legacy configuration file",
        "user=guest",
        "enable_logging=true",
        "last_modified=2019-08-12",
    ],
    "info.tmp": [
        "[INFO BLOCK]",
        "Session start: 2025-06-21 09:15",
        "Temporary cache: active",
        "User: ccri_admin",
    ],
    ".hint_file": [
        "# HINT: Sometimes things are not as they seem...",
        "Metadata may contain valuable information.",
        "Cross-check all hidden files carefully.",
    ],
    ".summary": [
        "=== Data Summary Report ===",
        "Total records processed: 1024",
        "Errors encountered: 0",
        "Exported successfully to archive.",
    ],
    "old.log": [
        "[2025-06-19 14:33:01] INFO User login attempt.",
        "[2025-06-19 14:34:11] DEBUG Connection established.",
        "[2025-06-19 14:35:22] WARN Disk usage at 92%.",
    ],
    ".keep.tmp": [
        "# Temporary Keep File",
        "Do not delete until verified by sysadmin.",
        "Checksum: a9b8c7d6e5f4",
    ],
    ".notes": [
        "Research notes for backup procedures.",
        "Remember to check permissions after restore.",
        "TODO: Document encryption key rotation.",
    ],
    "readme.txt": [
        "Welcome to the reference directory.",
        "This folder contains assorted documentation.",
        "Review each file carefully.",
    ],
    ".archive": [
        "# Archive header",
        "Compression method: gzip",
        "Created by archiver v2.1",
    ],
}

def generate_junk_for_file(file_name: str, flag: str = None) -> str:
    """
    Generate 3–7 lines of junk text for the specific file name,
    optionally embedding a flag.
    """
    base_name = file_name
    snippets = FILE_BASED_JUNK.get(base_name, ["# Generic placeholder content"])

    # Create junk content
    lines = random.choices(snippets, k=random.randint(3, 7))

    # Embed flag (or placeholder if no flag)
    insert_pos = random.randint(0, len(lines))
    if flag:
        lines.insert(insert_pos, flag)
    else:
        lines.insert(insert_pos, "# [No sensitive data found here]")

    return "\n".join(lines)

def create_folder_structure(base_dir: Path, real_flag: str, fake_flags: list):
    """
    Build the fixed folder structure and embed flags randomly in files.
    Create missing folders/files if necessary and overwrite contents.
    """
    base_dir.mkdir(parents=True, exist_ok=True)

    all_files = []

    # Create folders and files
    for folder_name, files in FOLDERS_AND_FILES.items():
        folder_path = base_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            file_path = folder_path / file_name
            all_files.append(file_path)

    # Randomly select 5 files for flags
    flag_files = random.sample(all_files, 5)
    real_flag_file = flag_files[0]
    fake_flag_files = flag_files[1:]

    # Write content to all files (create or overwrite)
    for file_path in all_files:
        if file_path == real_flag_file:
            content = generate_junk_for_file(file_path.name, real_flag)
        elif file_path in fake_flag_files:
            fake_flag = fake_flags.pop()
            content = generate_junk_for_file(file_path.name, fake_flag)
        else:
            content = generate_junk_for_file(file_path.name)
        file_path.write_text(content)

    print(f"✅ Real flag hidden in: {real_flag_file.relative_to(base_dir)}")
    print("📁 Folder structure created/updated with embedded flags.")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate the fixed folder structure with 1 real + 4 fake flags,
    and return the real flag.
    """
    real_flag = generate_real_flag()
    fake_flags = list({generate_fake_flag() for _ in range(4)})

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    create_folder_structure(challenge_folder / "junk", real_flag, fake_flags)
    return real_flag
