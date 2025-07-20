#!/usr/bin/env python3
import os
import sys
import time
from flag_generators.gen_03_rot13 import ROT13FlagGenerator  # ✅ Import animation function

# === ROT13 Decoder Helper ===

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
    cipher_file = os.path.join(script_dir, "cipher.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🔐 ROT13 Decoder Helper")
    print("===========================\n")
    print("📄 File to analyze: cipher.txt")
    print("🎯 Goal: Decode this message and find the hidden CCRI flag.\n")
    print("💡 What is ROT13?")
    print("   ➡️ A simple Caesar cipher that shifts each letter 13 places in the alphabet.")
    print("   ➡️ Encoding and decoding use the same operation because 13+13=26 (a full loop!).\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("We’ll use a Python helper to process each line:\n")
    print("   For every line in cipher.txt:")
    print("     ➡️ Rotate each letter forward by 13 places (A→N, N→A).\n")
    print("💻 The Python decoder also animates this process so you can watch it work.\n")
    pause("Press ENTER to launch the animated decoder...")

    # Check for cipher.txt existence
    if not os.path.isfile(cipher_file) or os.path.getsize(cipher_file) == 0:
        print("\n❌ ERROR: cipher.txt is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Read encoded message
    with open(cipher_file, "r") as f:
        encoded_lines = f.readlines()

    clear_screen()
    print("🔓 Decoding intercepted message...\n")

    # Animate line-by-line ROT13 transformation
    ROT13FlagGenerator.animate_rot13_line_by_line(encoded_lines, delay=0.05)

    # Fully decode for output file
    decoded_message = "".join([ROT13FlagGenerator.rot13(line) for line in encoded_lines])

    # Save decoded output
    with open(output_file, "w") as f_out:
        f_out.write(decoded_message + "\n")

    print("\n✅ Final Decoded Message saved to:")
    print(f"   📁 {output_file}\n")

    print("🧠 Look carefully: Only one string matches the CCRI flag format: CCRI-AAAA-1111")
    print("📋 Copy the correct flag and paste it into the scoreboard when ready.\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
