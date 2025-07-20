#!/usr/bin/env python3
import subprocess
import shutil
import sys
from pathlib import Path
import json

# === CCRI STEMDay Master Validator ===
VALIDATION_ROOT = Path.cwd() / "validation_results"
CHALLENGES_ROOT = Path.cwd() / "challenges"
CHALLENGES_JSON = Path.cwd() / "web_version_admin" / "challenges.json"

def clean_validation_folder():
    """Remove old validation results and create a fresh folder."""
    if VALIDATION_ROOT.exists():
        print("🧹 Cleaning old validation_results...")
        shutil.rmtree(VALIDATION_ROOT)
    VALIDATION_ROOT.mkdir()
    print("📁 Created fresh validation_results/ folder.")

def load_challenges_json():
    """Load challenges.json for real flags and script paths."""
    if not CHALLENGES_JSON.exists():
        print(f"❌ ERROR: {CHALLENGES_JSON} not found.", file=sys.stderr)
        sys.exit(1)
    with open(CHALLENGES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_challenge(challenge_id, entry):
    """Validate a single challenge."""
    print(f"\n🔍 Validating {challenge_id}: {entry['name']}...")
    original_folder = CHALLENGES_ROOT / entry["folder"]
    validation_folder = VALIDATION_ROOT / entry["folder"]
    validation_folder.mkdir(parents=True, exist_ok=True)

    # Copy challenge contents (except helper script)
    for item in original_folder.iterdir():
        if item.name != entry["script"]:
            if item.is_dir():
                shutil.copytree(item, validation_folder / item.name)
            else:
                shutil.copy2(item, validation_folder / item.name)

    # Run the helper script
    script_path = original_folder / entry["script"]
    if not script_path.exists():
        print(f"❌ ERROR: Helper script {script_path} not found.", file=sys.stderr)
        sys.exit(1)

    print(f"🚀 Running helper script: {script_path.name}")
    log_file = validation_folder / "validation.log"
    with open(log_file, "w", encoding="utf-8") as log:
        result = subprocess.run(
            ["python3", str(script_path)],
            cwd=validation_folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        log.write(result.stdout)

    if result.returncode != 0:
        print(f"❌ ERROR: Helper script failed for {challenge_id}. See {log_file}")
        sys.exit(1)

    # Check for the real flag in output
    expected_flag = entry["flag"]
    found_flag = None
    for line in result.stdout.splitlines():
        if expected_flag in line:
            found_flag = expected_flag
            break

    if not found_flag:
        print(f"❌ ERROR: Real flag '{expected_flag}' not found in script output for {challenge_id}.")
        print(f"   🔗 See {log_file} for details.")
        sys.exit(1)

    print(f"✅ {challenge_id}: Validation passed. Flag found = {found_flag}")

def main():
    print("\n🚦 CCRI STEMDay Master Validator\n" + "="*40)
    clean_validation_folder()
    challenges = load_challenges_json()
    for challenge_id, entry in challenges.items():
        validate_challenge(challenge_id, entry)

    print("\n🎉 All challenges validated successfully! The student workflow is working perfectly.\n")

if __name__ == "__main__":
    main()
