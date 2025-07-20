#!/usr/bin/env python3
import os
import subprocess
import sys

# === Base64 Decoder Helper ===

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
    input_file = os.path.join(script_dir, "encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🧩 Base64 Decoder Helper")
    print("===========================\n")
    print("📄 File to analyze: encoded.txt")
    print("🎯 Goal: Decode this file and find the hidden CCRI flag.\n")
    print("💡 What is Base64?")
    print("   ➡️ A text-based encoding scheme that turns binary data into readable text.")
    print("   Used to safely transmit data over systems that handle text better than raw binary.\n")
    print("🔧 We'll use the Linux tool 'base64' to reverse the encoding.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("To decode the file, we’ll run:\n")
    print("   base64 --decode encoded.txt\n")
    print("🔑 Breakdown:")
    print("   base64         → Call the Base64 tool")
    print("   --decode       → Switch from encoding to decoding")
    print("   encoded.txt    → Input file to decode\n")
    pause()

    # Simulate analysis
    print("\n🔍 Checking file for Base64 structure...")
    pause("Press ENTER to continue decoding...")
    print("✅ Structure confirmed!\n")
    print("⏳ Decoding content using:")
    print(f"   base64 --decode \"{input_file}\"\n")

    try:
        result = subprocess.run(
            ["base64", "--decode", input_file],
            capture_output=True,
            text=True,
            check=True
        )
        decoded = result.stdout.strip()
    except subprocess.CalledProcessError:
        print("\n❌ Decoding failed! This may not be valid Base64, or the file is corrupted.")
        print("💡 Tip: Ensure 'encoded.txt' exists and contains proper Base64 text.\n")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    if not decoded:
        print("\n❌ Decoding failed! No content was extracted.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Display and save decoded output
    print("\n📄 Decoded Message:")
    print("-----------------------------")
    print(decoded)
    print("-----------------------------")
    with open(output_file, "w") as f:
        f.write(decoded + "\n")

    print(f"\n📁 Decoded output saved as: {output_file}")
    print("🔎 Look for a string matching this format: CCRI-AAAA-1111")
    print("🧠 This is your flag. Copy it into the scoreboard!\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
