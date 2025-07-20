#!/usr/bin/env python3
import os
import subprocess
import sys

# === Stego Decode Helper ===

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
    target_image = os.path.join(script_dir, "squirrel.jpg")
    decoded_file = os.path.join(script_dir, "decoded_message.txt")

    clear_screen()
    print("🕵️ Stego Decode Helper")
    print("==========================\n")
    print("🎯 Target image: squirrel.jpg")
    print("🔍 Tool: steghide\n")
    print("💡 What is steghide?")
    print("   ➡️ A Linux tool that can HIDE or EXTRACT secret data inside images or audio files.")
    print("   We'll use it to try and extract a hidden message from squirrel.jpg.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("When we try a password, this command will run:\n")
    print("   steghide extract -sf squirrel.jpg -xf decoded_message.txt -p [your password]\n")
    print("🔑 Breakdown:")
    print("   -sf squirrel.jpg          → Stego file (the image to scan)")
    print("   -xf decoded_message.txt   → Extract to this file")
    print("   -p [password]             → Try this password for extraction\n")
    pause()

    while True:
        pw = input("🔑 Enter a password to try (or type 'exit' to quit): ").strip()

        if not pw:
            print("⚠️ You must enter something. Try again.\n")
            continue

        if pw.lower() == "exit":
            print("\n👋 Exiting... good luck on your next mission!")
            pause("Press ENTER to close this window...")
            sys.exit(0)

        print(f"\n🔓 Trying password: {pw}")
        print("📦 Scanning squirrel.jpg for hidden data...\n")
        print(f"💻 Running: steghide extract -sf \"{target_image}\" -xf \"{decoded_file}\" -p \"{pw}\"\n")

        # Attempt extraction
        try:
            result = subprocess.run(
                ["steghide", "extract", "-sf", target_image, "-xf", decoded_file, "-p", pw, "-f"],
                input=b"\n",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("❌ ERROR: steghide is not installed or not in PATH.")
            sys.exit(1)

        if os.path.exists(decoded_file) and os.path.getsize(decoded_file) > 0:
            print("🎉 ✅ SUCCESS! Hidden message recovered:")
            print("----------------------------")
            with open(decoded_file, "r") as f:
                print(f.read())
            print("----------------------------")
            print("📁 Saved as decoded_message.txt in this folder")
            print("💡 Look for a string like CCRI-ABCD-1234 to use as your flag.\n")
            pause("Press ENTER to close this terminal...")
            sys.exit(0)
        else:
            print("❌ Extraction failed. No hidden data or incorrect password.")
            print("🔁 Try again with a different password.\n")
            if os.path.exists(decoded_file):
                os.remove(decoded_file)

if __name__ == "__main__":
    main()
