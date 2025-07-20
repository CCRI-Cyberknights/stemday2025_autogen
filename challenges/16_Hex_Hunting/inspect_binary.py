#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time

# === Hex Flag Hunter Helper ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

def scanning_animation():
    if not validation_mode:
        print("\n🔎 Scanning binary for flag-like patterns", end="", flush=True)
        for _ in range(5):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print()

def search_flags(binary_file, pattern=r"CCRI-[A-Z]{4}-[0-9]{4}"):
    try:
        grep_output = subprocess.run(
            ["grep", "-aboE", pattern, binary_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if grep_output.returncode != 0:
            return []
        flags = []
        for line in grep_output.stdout.strip().splitlines():
            _, _, flag = line.partition(":")
            flags.append(flag.strip())
        return flags
    except Exception as e:
        print(f"❌ Error while scanning binary: {e}")
        sys.exit(1)

def validate_flag_in_binary(binary_file, expected_flag):
    print("🔍 Validation: scanning hex_flag.bin for expected flag...")
    flags = search_flags(binary_file)
    if expected_flag in flags:
        print(f"✅ Validation success: found flag {expected_flag}")
        return True
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found", file=sys.stderr)
        return False

def show_hex_context(binary_file, offset, length=64):
    start = max(offset - 16, 0)
    print(f"📖 Hex context (around offset {offset}):")
    print("   Command used:")
    print(f"   dd if={os.path.basename(binary_file)} bs=1 skip={start} count={length} | xxd")
    time.sleep(1)
    try:
        dd_process = subprocess.Popen(
            ["dd", f"if={binary_file}", "bs=1", f"skip={start}", f"count={length}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        xxd_process = subprocess.Popen(
            ["xxd"],
            stdin=dd_process.stdout,
            text=True
        )
        dd_process.stdout.close()
        xxd_process.communicate()
    except FileNotFoundError:
        print("❌ ERROR: dd or xxd command not found on this system.")

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    binary_file = os.path.join(script_dir, "hex_flag.bin")
    notes_file = os.path.join(script_dir, "notes.txt")

    if validation_mode:
        # Load expected flag from validation unlocks
        unlock_file = os.path.join(project_root, "web_version_admin", "validation_unlocks.json")
        try:
            with open(unlock_file, "r", encoding="utf-8") as f:
                unlocks = json.load(f)
            expected_flag = unlocks["16_Hex_Hunting"]["real_flag"]
        except Exception as e:
            print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
            sys.exit(1)

        # Validate
        if validate_flag_in_binary(binary_file, expected_flag):
            sys.exit(0)
        else:
            sys.exit(1)

    # === Student Interactive Mode ===
    clear_screen()
    print("🔍 Hex Flag Hunter")
    print("============================\n")
    print("🎯 Target binary: hex_flag.bin\n")
    print("💡 Goal: Locate the real flag (format: CCRI-AAAA-1111).")
    print("    ⚠️ 5 candidate flags are embedded, but only ONE is correct!\n")
    print("🔧 Behind the scenes:")
    print("   We'll scan the binary for any strings that *look like* flags using 'grep'.")
    print("   Then we'll preview surrounding bytes in hex for context with 'xxd' and 'dd'.\n")
    pause()

    if not os.path.isfile(binary_file):
        print(f"❌ ERROR: {os.path.basename(binary_file)} not found in this folder!")
        pause("Press ENTER to exit...")
        sys.exit(1)

    scanning_animation()
    flags = search_flags(binary_file)

    if not flags:
        print("\n❌ No flag-like patterns found. Exiting...")
        pause()
        sys.exit(1)

    print(f"\n✅ Found {len(flags)} candidate flag(s).\n")

    # Clear old notes file
    open(notes_file, "w").close()

    for idx, flag in enumerate(flags, 1):
        print("--------------------------------------------")
        print(f"[{idx}/{len(flags)}] Candidate Flag: {flag}")
        print("--------------------------------------------")

        # Find offset
        grep_offset = subprocess.run(
            ["grep", "-abo", flag, binary_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if grep_offset.returncode != 0:
            print(f"⚠️ Could not determine offset for {flag}")
            continue
        offset = int(grep_offset.stdout.partition(":")[0])

        # Show hex dump
        show_hex_context(binary_file, offset)

        # Options for the user
        while True:
            print("\nOptions:")
            print("1) ✅ Mark this flag as POSSIBLE and save to notes.txt")
            print("2) ➡️ Skip to next flag")
            print("3) 🚪 Quit investigation\n")
            choice = input("Choose an option (1-3): ").strip()
            if choice == "1":
                with open(notes_file, "a") as f:
                    f.write(flag + "\n")
                print(f"✅ Saved '{flag}' to notes.txt")
                time.sleep(0.5)
                break
            elif choice == "2":
                print("➡️ Skipping to next candidate...")
                time.sleep(0.5)
                break
            elif choice == "3":
                print("\n👋 Exiting investigation early.")
                print(f"📁 All saved candidate flags are in {os.path.basename(notes_file)}")
                pause()
                sys.exit(0)
            else:
                print("⚠️ Invalid choice. Please enter 1, 2, or 3.")

        print()

    print("🎉 Investigation complete!")
    print(f"📁 All saved candidate flags are in {os.path.basename(notes_file)}")
    print("📝 Review and submit the correct flag to the scoreboard!")
    pause()

if __name__ == "__main__":
    validation_mode = os.getenv("CCRI_VALIDATE") == "1"
    main()
