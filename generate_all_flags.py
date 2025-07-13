#!/usr/bin/env python3

import json
import argparse
from pathlib import Path

# === CONFIGURATION ===
BASE_DIR = Path(__file__).parent.resolve()
CHALLENGES_JSON = BASE_DIR / "web_version_admin/challenges.json"
CHALLENGES_DIR = BASE_DIR / "challenges/"
DRYRUN_DIR = BASE_DIR / "dryrun_output/"

# === Import all generators ===
from flag_generators.gen_01_stego import generate_flag as gen_01
from flag_generators.gen_02_base64 import generate_flag as gen_02
from flag_generators.gen_03_rot13 import generate_flag as gen_03
from flag_generators.gen_04_vigenere import generate_flag as gen_04
from flag_generators.gen_05_archive_password import generate_flag as gen_05
from flag_generators.gen_06_hashcat import generate_flag as gen_06
from flag_generators.gen_07_extract_binary import generate_flag as gen_07
from flag_generators.gen_08_fake_auth_log import generate_flag as gen_08
from flag_generators.gen_09_fix_script import generate_flag as gen_09
from flag_generators.gen_10_metadata import generate_flag as gen_10
from flag_generators.gen_11_hidden_flag import generate_flag as gen_11
from flag_generators.gen_12_qr_codes import generate_flag as gen_12
from flag_generators.gen_13_http_headers import generate_flag as gen_13
from flag_generators.gen_14_subdomain_sweep import generate_flag as gen_14
from flag_generators.gen_15_process_inspection import generate_flag as gen_15
from flag_generators.gen_16_hex_hunting import generate_flag as gen_16
from flag_generators.gen_17_nmap_scanning import generate_flag as gen_17
from flag_generators.gen_18_pcap_search import generate_flag as gen_18

GENERATOR_MAP = {
    "01_Stego": gen_01,
    "02_Base64": gen_02,
    "03_ROT13": gen_03,
    "04_Vigenere": gen_04,
    "05_ArchivePassword": gen_05,
    "06_Hashcat": gen_06,
    "07_ExtractBinary": gen_07,
    "08_FakeAuthLog": gen_08,
    "09_FixScript": gen_09,
    "10_Metadata": gen_10,
    "11_HiddenFlag": gen_11,
    "12_QRCodes": gen_12,
    "13_HTTPHeaders": gen_13,
    "14_SubdomainSweep": gen_14,
    "15_ProcessInspection": gen_15,
    "16_Hex_Hunting": gen_16,
    "17_Nmap_Scanning": gen_17,
    "18_Pcap_Search": gen_18,
}

# === Master Flag Generation ===
def main(dry_run=False):
    # Load challenges.json
    with open(CHALLENGES_JSON, "r") as f:
        challenges = json.load(f)

    if dry_run:
        print("📝 Dry-run mode enabled: outputs will be written to 'dryrun_output/'\n")
        DRYRUN_DIR.mkdir(exist_ok=True)

    for challenge_id, challenge in challenges.items():
        # Use dummy folder if dry-run, otherwise use real challenge folder
        live_folder = (CHALLENGES_DIR / Path(challenge["folder"]).name).resolve()
        dry_folder = (DRYRUN_DIR / Path(challenge["folder"]).name).resolve()
        target_folder = dry_folder if dry_run else live_folder
        target_folder.mkdir(parents=True, exist_ok=True)

        print(f"🚀 Generating flag for {challenge_id}...")

        if challenge_id in GENERATOR_MAP:
            real_flag = GENERATOR_MAP[challenge_id](target_folder)
            if dry_run:
                print(f"✅ [Dry-Run] {challenge_id}: Real flag = {real_flag}")
                print(f"📂 Would write files to: {target_folder}")
                print(f"📄 Would update challenges.json with: {real_flag}\n")
            else:
                challenge["flag"] = real_flag
                print(f"✅ {challenge_id}: Real flag = {real_flag}\n")
        else:
            print(f"⚠️ No generator found for {challenge_id}. Skipping.\n")

    if dry_run:
        print("✅ Dry-run complete. No changes made to live challenges or challenges.json.")
    else:
        # Save updated challenges.json
        with open(CHALLENGES_JSON, "w") as f:
            json.dump(challenges, f, indent=4)
        print("🎉 All flags generated and challenges.json updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate flags for all challenges.")
    parser.add_argument("--dry-run", action="store_true", help="Run without modifying challenges.json or live challenge folders")
    args = parser.parse_args()

    main(dry_run=args.dry_run)
