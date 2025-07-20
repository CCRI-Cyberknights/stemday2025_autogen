#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === ZIP Password Cracking Challenge ===

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

def progress_bar(length=30, delay=0.03):
    for _ in range(length):
        print("█", end="", flush=True)
        time.sleep(delay)
    print()

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    cipher_zip = os.path.join(script_dir, "secret.zip")
    wordlist = os.path.join(script_dir, "wordlist.txt")
    extracted_b64 = os.path.join(script_dir, "message_encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🔓 ZIP Password Cracking Challenge")
    print("======================================\n")
    print("📁 Target archive: secret.zip")
    print("📜 Wordlist: wordlist.txt\n")
    print("🎯 Goal: Crack the ZIP file’s password and decode the message inside.\n")
    print("💡 How this works:")
    print("   ➡️ We’ll test each password in wordlist.txt by running:\n")
    print("      unzip -P [password] -t secret.zip\n")
    print("   🛠 Breakdown:")
    print("      -P [password] → Supplies the password")
    print("      -t            → Tests if the ZIP is valid without extracting\n")
    pause()

    # Pre-flight checks
    if not os.path.isfile(cipher_zip):
        print("❌ ERROR: secret.zip not found in this folder.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    if not os.path.isfile(wordlist):
        print("❌ ERROR: wordlist.txt not found in this folder.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    found = False
    correct_pass = ""

    print("\n🔍 Starting password scan...\n")
    time.sleep(0.5)

    # Try each password
    with open(wordlist, "r") as wl:
        for pw in wl:
            pw = pw.strip()
            print(f"\r[🔐] Trying password: {pw:<20}", end="", flush=True)
            time.sleep(0.05)
            try:
                result = subprocess.run(
                    ["unzip", "-P", pw, "-t", cipher_zip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if "OK" in result.stdout:
                    print(f"\n\n✅ Password found: \"{pw}\"")
                    correct_pass = pw
                    found = True
                    break
            except FileNotFoundError:
                print("\n❌ ERROR: 'unzip' command not found.")
                sys.exit(1)

    if not found:
        print("\n❌ Password not found in wordlist.txt.")
        print("💡 Tip: You might need a bigger or different wordlist.\n")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Confirm extraction
    go = input("\nDo you want to extract the ZIP archive now? [Y/n] ").strip().lower()
    if go == "n":
        sys.exit(0)

    print("\n📦 Extracting secret.zip...")
    try:
        subprocess.run(
            ["unzip", "-P", correct_pass, cipher_zip, "-d", script_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("\n❌ ERROR: 'unzip' command not found.")
        sys.exit(1)

    if not os.path.isfile(extracted_b64):
        print("❌ Extraction failed.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Display Base64 content
    print("\n📄 Extracted Base64 Data:")
    print("-------------------------------")
    with open(extracted_b64, "r") as f:
        print(f.read())
    print("-------------------------------\n")

    # Prompt for decoding
    decode = input("Would you like to decode the Base64 message now? [Y/n] ").strip().lower()
    if decode == "n":
        print("\n⚠️ Skipping Base64 decoding. You can run:")
        print(f"    base64 --decode \"{extracted_b64}\"")
        print("later if needed.\n")
        pause("Press ENTER to close this terminal...")
        sys.exit(0)

    # Decoding phase
    print("\n🧪 Base64 Detected!")
    print("   Base64 encodes binary data as text for safe transmission.\n")
    print(f"🔓 Decoding Base64 using:")
    print(f"    base64 --decode \"{extracted_b64}\"\n")
    pause("Press ENTER to start decoding...")

    print("\n🔽 Decoding...")
    progress_bar()

    try:
        result = subprocess.run(
            ["base64", "--decode", extracted_b64],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        decoded = result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Decoding failed. The file may not be valid Base64.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Display decoded message
    print("\n🧾 Decoded Message:")
    print("-------------------------------")
    print(decoded)
    print("-------------------------------\n")

    # Save decoded output
    with open(output_file, "w") as f_out:
        f_out.write(decoded + "\n")
    print(f"💾 Decoded output saved as: {output_file}\n")
    print("🧠 Find the CCRI flag (format: CCRI-AAAA-1111) and submit it to the scoreboard.")

    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
