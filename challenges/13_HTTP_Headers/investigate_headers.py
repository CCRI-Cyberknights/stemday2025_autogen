#!/usr/bin/env python3
import os
import sys
import subprocess

# === HTTP Headers Mystery ===

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

def check_response_files(files):
    missing = []
    for f in files:
        if not os.path.isfile(f):
            print(f"❌ ERROR: '{os.path.basename(f)}' not found!")
            missing.append(f)
    return missing

def view_file_with_less(file_path):
    try:
        subprocess.run(["less", file_path])
    except FileNotFoundError:
        print("❌ ERROR: 'less' command not found on this system.")
        sys.exit(1)

def bulk_scan_for_flags(script_dir):
    try:
        result = subprocess.run(
            ["grep", "-E", "CCRI-[A-Z]{4}-[0-9]{4}", os.path.join(script_dir, "response_*.txt")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        if result.stdout:
            print(result.stdout)
        else:
            print("⚠️ No flags found in bulk scan.")
    except Exception as e:
        print(f"❌ ERROR during bulk scan: {e}")

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    responses = [os.path.join(script_dir, f"response_{i}.txt") for i in range(1, 6)]

    clear_screen()
    print("📡 HTTP Headers Mystery")
    print("=================================\n")
    print("🎯 Mission Briefing:")
    print("---------------------------------")
    print("You've intercepted **five HTTP responses** during a network investigation.")
    print("The real flag is hidden in one of their HTTP headers.\n")
    print("🧠 Flag format: CCRI-AAAA-1111")
    print("💡 Tip: HTTP headers are key-value pairs sent by a server along with its response.")
    print("        We can view and search for hidden data inside them.\n")

    # Pre-flight check
    missing_files = check_response_files(responses)
    if missing_files:
        pause("\n⚠️ Missing one or more response files. Press ENTER to exit.")
        sys.exit(1)

    while True:
        print("\n📂 Available HTTP responses:")
        for i, response in enumerate(responses, 1):
            print(f"{i}. {os.path.basename(response)}")
        print("6. Bulk scan all files for flag-like patterns")
        print("7. Exit\n")

        choice = input("Select an option (1-7): ").strip()

        if choice in {"1", "2", "3", "4", "5"}:
            idx = int(choice) - 1
            file = responses[idx]
            print(f"\n🔍 Opening {os.path.basename(file)} (press 'q' to quit)...")
            print("---------------------------------")
            print("💻 Tip: Press '/' to search within the file for 'CCRI-'\n")
            view_file_with_less(file)
            print("---------------------------------")

        elif choice == "6":
            print("\n🔎 Bulk scanning all HTTP headers for flag patterns...")
            print("💻 Running: grep -E 'CCRI-[A-Z]{4}-[0-9]{4}' response_*.txt\n")
            bulk_scan_for_flags(script_dir)
            pause("\nPress ENTER to return to the menu.")

        elif choice == "7":
            print("\n👋 Exiting HTTP Headers Mystery. Stay sharp, agent!")
            break

        else:
            print("\n❌ Invalid option. Please select a number from 1 to 7.")
            pause()

if __name__ == "__main__":
    main()
