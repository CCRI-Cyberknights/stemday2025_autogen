#!/usr/bin/env python3
import os
import sys
import time

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

def rot13_char(c):
    if 'a' <= c <= 'z':
        return chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':
        return chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
    else:
        return c

def animate_rot13(encoded_text):
    decoded_chars = list(encoded_text)
    for i in range(len(encoded_text)):
        c = encoded_text[i]
        if c.isalpha():
            for step in range(13):
                rotated = chr(((ord(c.lower()) - ord('a') + step) % 26 + ord('a')))
                if c.isupper():
                    rotated = rotated.upper()
                decoded_chars[i] = rotated
                clear_screen()
                print("🔐 ROT13 Decoder Helper")
                print("===========================\n")
                print("🌀 Decrypting:\n")
                print("".join(decoded_chars))
                time.sleep(0.02)
            decoded_chars[i] = rot13_char(c)
    return "".join(decoded_chars)

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
    print("We’ll use a Python helper to process each character:\n")
    print("   For every letter in cipher.txt:")
    print("     ➡️ Rotate it forward by 13 places (A→N, N→A).\n")
    print("💻 The Python decoder also animates this process so you can watch it work.\n")
    pause("Press ENTER to launch the animated decoder...")

    # Check for cipher.txt existence
    if not os.path.isfile(cipher_file) or os.path.getsize(cipher_file) == 0:
        print("\n❌ ERROR: cipher.txt is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    with open(cipher_file, "r") as f:
        encoded = f.read()

    final_message = animate_rot13(encoded)

    # Save decoded output
    with open(output_file, "w") as f_out:
        f_out.write(final_message + "\n")

    clear_screen()
    print("✅ Final Decoded Message:")
    print("-----------------------------")
    print(final_message)
    print("-----------------------------")
    print(f"📁 Saved to: {output_file}\n")

    print("🧠 Look carefully: Only one string matches the CCRI flag format: CCRI-AAAA-1111")
    print("📋 Copy the correct flag and paste it into the scoreboard when ready.\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
