#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Hashcat ChainCrack Demo ===

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

def print_progress_bar(length=30, delay=0.02):
    for _ in range(length):
        print("█", end="", flush=True)
        time.sleep(delay)
    print()

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    hashes_file = os.path.join(script_dir, "hashes.txt")
    wordlist_file = os.path.join(script_dir, "wordlist.txt")
    potfile = os.path.join(script_dir, "hashcat.potfile")
    segments_dir = os.path.join(script_dir, "segments")
    extracted_dir = os.path.join(script_dir, "extracted")
    decoded_dir = os.path.join(script_dir, "decoded_segments")
    assembled_file = os.path.join(script_dir, "assembled_flag.txt")

    clear_screen()
    print("🔓 Hashcat ChainCrack Demo")
    print("===============================\n")
    print("📂 Hashes to crack:     hashes.txt")
    print("📖 Wordlist to use:     wordlist.txt")
    print("📦 Encrypted segments:  segments/part*.zip\n")
    print("🎯 Goal: Crack all 3 hashes, unlock 3 ZIP segment files, decode them, and reassemble the flag!\n")
    print("💡 What’s happening here?")
    print("   ➡️ Hashcat will match words from the wordlist to hash values (like solving digital locks).")
    print("   ➡️ Each cracked hash unlocks a ZIP segment file.")
    print("   ➡️ Segments contain base64-encoded data we'll need to decode and stitch together.\n")
    pause()

    # Pre-flight checks
    if not os.path.isfile(hashes_file) or not os.path.isfile(wordlist_file):
        print("❌ ERROR: Required files hashes.txt or wordlist.txt are missing.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    if not os.path.isdir(segments_dir):
        print("❌ ERROR: Segments folder is missing.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Clean up any old results
    print("\n[🧹] Clearing previous Hashcat outputs and decoded data...")
    for path in [potfile, assembled_file]:
        if os.path.exists(path):
            os.remove(path)
    for directory in [extracted_dir, decoded_dir]:
        if os.path.exists(directory):
            subprocess.run(["rm", "-rf", directory])
    os.makedirs(extracted_dir, exist_ok=True)
    os.makedirs(decoded_dir, exist_ok=True)

    # Explain hashcat
    print("\n🛠️ Behind the Scenes: Hashcat Command")
    print("-------------------------------------------")
    print("hashcat -m 0 -a 0 hashes.txt wordlist.txt")
    print("   -m 0 = MD5 hash mode")
    print("   -a 0 = dictionary attack (uses wordlist.txt)")
    print("   --potfile-path = where cracked hashes are stored\n")
    pause("Press ENTER to launch Hashcat...")

    # Run hashcat
    subprocess.run(
        ["hashcat", "-m", "0", "-a", "0", hashes_file, wordlist_file, "--potfile-path", potfile, "--force"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("\n[✅] Hashcat finished cracking. Cracked hashes:")
    cracked = {}
    with open(potfile, "r") as pf:
        for line in pf:
            if ':' in line:
                hash_val, password = line.strip().split(':', 1)
                cracked[hash_val] = password
                print(f"🔓 {hash_val} : {password}")

    pause("\nPress ENTER to extract and decode encrypted ZIP segments...")

    # Mapping hashes to zip files
    hash_to_file = {
        "4e14b4bed16c945384faad2365913886": "part1.zip",  # brightmail
        "ceabb18ea6bbce06ce83664cf46d1fa8": "part2.zip",  # letacla
        "08f5b04545cbf7eaa238621b9ab84734": "part3.zip",  # Password12
    }

    # Extract segments and decode
    for hash_val, password in cracked.items():
        zipfile = hash_to_file.get(hash_val)
        if not zipfile:
            print(f"❌ No ZIP mapping found for hash: {hash_val}")
            continue

        print(f"\n🔑 Unlocking {zipfile} with password: {password}")
        subprocess.run(
            ["unzip", "-P", password, os.path.join(segments_dir, zipfile), "-d", extracted_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Find and decode base64 segment
        segment_files = [f for f in os.listdir(extracted_dir) if f.lower().startswith("encoded_segment")]
        for segment_file in segment_files:
            seg_path = os.path.join(extracted_dir, segment_file)
            decoded_path = os.path.join(decoded_dir, f"decoded_{os.path.splitext(segment_file)[0]}.txt")

            print(f"✅ Extracted encoded segment: {segment_file}")
            print("ℹ️  This file uses Base64 encoding. Let's decode it to reveal the real content.")
            time.sleep(0.5)
            print(f"\n🔽 Decoding Base64 with: base64 --decode \"{seg_path}\"")
            time.sleep(0.5)

            try:
                result = subprocess.run(
                    ["base64", "--decode", seg_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                with open(decoded_path, "w") as df:
                    df.write(result.stdout)
                print(f"📄 Decoded → {decoded_path}")
                print("-----------------------------")
                print(result.stdout.strip())
                print("-----------------------------")
            except subprocess.CalledProcessError:
                print(f"⚠️  Decoding failed for: {seg_path}")

    # Assemble flag from decoded segments
    print("\n🧩 Reassembling final flag...")
    time.sleep(1)
    decoded_files = sorted([f for f in os.listdir(decoded_dir) if f.endswith(".txt")])

    if len(decoded_files) == 3:
        with open(assembled_file, "w") as out_f:
            for i in range(5):
                part1 = open(os.path.join(decoded_dir, decoded_files[0])).readlines()[i].strip()
                part2 = open(os.path.join(decoded_dir, decoded_files[1])).readlines()[i].strip()
                part3 = open(os.path.join(decoded_dir, decoded_files[2])).readlines()[i].strip()
                flag = f"{part1}-{part2}-{part3}"
                print(f"- {flag}")
                out_f.write(flag + "\n")
        print(f"\n✅ All candidate flags saved to: {assembled_file}")
    else:
        print("❌ One or more decoded segments are missing. Cannot assemble final flags.")

    pause("\n🔎 Review the candidate flags above. Only ONE matches the CCRI format: CCRI-AAAA-1111\nPress ENTER to close this terminal...")

if __name__ == "__main__":
    main()
