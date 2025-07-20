#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Auth Log Investigation Helper ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    log_file = os.path.join(script_dir, "auth.log")
    candidates_file = os.path.join(script_dir, "flag_candidates.txt")

    clear_screen()
    print("🕵️‍♂️ Auth Log Investigation")
    print("==============================\n")
    print("📄 Target file: auth.log")
    print("🔧 Tool in use: grep\n")
    print("🎯 Goal: Identify a suspicious login record by analyzing fake auth logs.")
    print("   ➡️ One of these records contains a **PID** that hides the real flag!\n")
    print("💡 Why grep?")
    print("   ➡️ 'grep' helps us search for patterns in large text files.")
    print("   ➡️ We'll look for strange PIDs (e.g., ones containing dashes or letters).\n")
    pause()

    # Check for auth.log
    if not os.path.isfile(log_file):
        print(f"\n❌ ERROR: auth.log not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Show preview
    print("\n📄 Preview: First 10 lines from auth.log")
    print("-------------------------------------------")
    try:
        with open(log_file, "r") as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                print(line.strip())
    except FileNotFoundError:
        print("❌ ERROR: Could not open auth.log.")
        sys.exit(1)
    print("-------------------------------------------\n")
    pause("Press ENTER to scan for suspicious entries...")

    # Scan for suspicious PID patterns
    print("\n🔍 Scanning for entries with unusual PID patterns (e.g., [CCRI-XXXX-1234] or containing dashes)...")
    time.sleep(0.5)
    match_pattern = r"\[[A-Z0-9\-]{8,}\]"
    try:
        with open(candidates_file, "w") as out_f:
            subprocess.run(
                ["grep", "-E", match_pattern, log_file],
                stdout=out_f,
                stderr=subprocess.DEVNULL
            )
    except Exception as e:
        print(f"❌ ERROR while scanning: {e}")
        sys.exit(1)

    try:
        with open(candidates_file, "r") as f:
            lines = f.readlines()
        cand_count = len(lines)
    except FileNotFoundError:
        cand_count = 0

    if cand_count == 0:
        print("⚠️ No suspicious entries found in auth.log.")
        pause("Press ENTER to close this terminal...")
        sys.exit(0)

    print(f"\n📌 Found {cand_count} potential suspicious line(s).")
    print(f"💾 Saved to: {candidates_file}\n")

    # Preview suspicious lines
    pause("Press ENTER to preview suspicious entries...")
    print("\n-------------------------------------------")
    for i, line in enumerate(lines):
        if i >= 5:
            print("... (only first 5 shown)")
            break
        print(line.strip())
    print("-------------------------------------------\n")

    # Optional search
    pattern = input("🔎 Enter a username, IP, or keyword to search in the full log (or press ENTER to skip): ").strip()
    if pattern:
        print(f"\n🔎 Searching for '{pattern}' in auth.log...")
        try:
            subprocess.run(
                ["grep", "--color=always", pattern, log_file],
                check=False
            )
        except FileNotFoundError:
            print("❌ ERROR: grep command not found.")
    else:
        print("⏭️  Skipping custom search.")

    # Wrap-up
    print("\n🧠 Hint: One of the flagged PIDs hides the official flag!")
    print("   Format: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
