#!/usr/bin/env python3
import os
import sys

# === Vigenère Cipher Breaker ===

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

def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.lower()
    key_len = len(key)
    key_indices = [ord(k) - ord('a') for k in key]
    key_pos = 0

    for char in ciphertext:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            pi = ord(char) - offset
            ki = key_indices[key_pos % key_len]
            decrypted = chr((pi - ki) % 26 + offset)
            result.append(decrypted)
            key_pos += 1
        else:
            result.append(char)
    return ''.join(result)

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    cipher_file = os.path.join(script_dir, "cipher.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🔐 Vigenère Cipher Breaker")
    print("===============================\n")
    print("📄 Encrypted message: cipher.txt")
    print("🎯 Goal: Decrypt it and find the CCRI flag.\n")
    print("💡 What is Vigenère?")
    print("   ➡️ A cipher that uses a repeating keyword to shift each letter.")
    print("   ➡️ For example, with keyword 'KEY':")
    print("         Plain:  HELLO WORLD")
    print("         Cipher: RIJVS UYVJN\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("-----------------------------")
    print("We’ll use this Python helper:\n")
    print("   python3 vigenere_decode.py [keyword]\n")
    print("🔑 It reverses the shifting pattern based on your keyword.")
    print("   If the keyword is correct, the flag will appear!\n")
    pause("Press ENTER to begin keyword testing...")

    if not os.path.isfile(cipher_file):
        print("❌ ERROR: cipher.txt not found in this folder.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    with open(cipher_file, "r") as f:
        ciphertext = f.read()

    while True:
        key = input("🔑 Enter a keyword to try (or type 'exit' to quit): ").strip()

        if key.lower() == "exit":
            print("\n👋 Exiting. Stay sharp, Agent!")
            break

        if not key:
            print("⚠️ Please enter a keyword or type 'exit'.\n")
            continue

        print(f"\n🔓 Attempting decryption with keyword: {key}")
        plaintext = vigenere_decrypt(ciphertext, key)

        print("\n📄 Decoded Output:")
        print("-----------------------------")
        print(plaintext)
        print("-----------------------------\n")

        # Save output
        with open(output_file, "w") as f_out:
            f_out.write(plaintext)

        if "CCRI-" in plaintext:
            print("✅ Flag found in decrypted text!")
            print(f"📁 Saved to: {output_file}")
            print("📋 Copy the CCRI flag and submit it on the scoreboard.\n")
            break
        else:
            print("❌ No valid CCRI flag format detected.\n")
            again = input("🔁 Try another keyword? (Y/n): ").strip().lower()
            if again == "n":
                break

    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
