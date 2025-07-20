#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Binary Forensics Challenge ===

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
    target_binary = os.path.join(script_dir, "hidden_flag")
    outfile = os.path.join(script_dir, "extracted_strings.txt")
    temp_matches = os.path.join(script_dir, "temp_matches.txt")

    clear_screen()
    print("🧪 Binary Forensics Challenge")
    print("=============================\n")
    print("📦 Target binary: hidden_flag")
    print("🔧 Tool in use: strings\n")
    print("🎯 Goal: Uncover a hidden flag embedded inside this compiled program.\n")
    print("💡 Why use 'strings'?")
    print("   ➡️ 'strings' scans binary files and extracts any readable text sequences.")
    print("   ➡️ Often used to find debugging info, secret keys, or flags left behind.\n")
    pause()

    # Pre-flight check
    if not os.path.isfile(target_binary):
        print(f"\n❌ ERROR: The file 'hidden_flag' was not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Run strings and save results
    print(f"\n🔍 Running: strings \"{target_binary}\" > \"{outfile}\"")
    try:
        with open(outfile, "w") as out_f:
            subprocess.run(["strings", target_binary], stdout=out_f, check=True)
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to run 'strings'.")
        sys.exit(1)
    time.sleep(0.5)
    print(f"✅ All extracted strings saved to: {outfile}\n")

    # Preview some output
    preview_lines = 15
    print(f"📄 Previewing the first {preview_lines} lines of extracted text:")
    print("--------------------------------------------------")
    try:
        with open(outfile, "r") as f:
            for i, line in enumerate(f):
                if i >= preview_lines:
                    break
                print(line.strip())
    except FileNotFoundError:
        print("❌ ERROR: Could not open extracted_strings.txt.")
    print("--------------------------------------------------\n")
    pause("Press ENTER to scan for flag patterns...")

    # Search for flag patterns
    print("🔎 Scanning for flag-like patterns (format: XXXX-YYYY-ZZZZ)...")
    time.sleep(0.5)
    match_pattern = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'
    try:
        with open(outfile, "r") as f_in, open(temp_matches, "w") as f_out:
            matches = []
            for line in f_in:
                if subprocess.run(
                    ["grep", "-E", match_pattern],
                    input=line.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL
                ).stdout:
                    matches.append(line.strip())
                    f_out.write(line)
        count = len(matches)
    except Exception as e:
        print(f"❌ ERROR while scanning: {e}")
        sys.exit(1)

    if count > 0:
        print(f"\n📌 Found {count} possible flag(s) matching that format!")
    else:
        print("\n⚠️ No obvious flags found. Try scanning manually in extracted_strings.txt.")

    # Optional keyword search
    print()
    keyword = input("🔍 Enter a keyword to search in the full dump (or hit ENTER to skip): ").strip()
    if keyword:
        print(f"\n🔎 Searching for '{keyword}' in {outfile}...")
        try:
            result = subprocess.run(
                ["grep", "-i", "--color=always", keyword, outfile],
                check=False
            )
            if result.returncode != 0:
                print(f"❌ No matches for '{keyword}'.")
        except FileNotFoundError:
            print("❌ ERROR: grep command not found.")
    else:
        print("⏭️  Skipping keyword search.")

    # Wrap-up
    print("\n✅ Done! You can inspect extracted_strings.txt further or try other tools like 'hexdump' for deeper analysis.")
    print("🧠 Remember: Only one string matches the official flag format: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
