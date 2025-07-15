#!/usr/bin/env python3

from pathlib import Path
import random
import sys
from flag_generators.flag_helpers import generate_real_flag  # ✅ no need for generate_fake_flag here

ALL_OPERATORS = ["+", "-", "*", "/"]

# === Helper: Find Project Root ===
def find_project_root() -> Path:
    """
    Walk up directories until .ccri_ctf_root is found.
    """
    dir_path = Path.cwd()
    for parent in [dir_path] + list(dir_path.parents):
        if (parent / ".ccri_ctf_root").exists():
            return parent.resolve()
    print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
    sys.exit(1)

# === Resolve Project Root ===
PROJECT_ROOT = find_project_root()


def find_safe_parts_and_operator():
    """
    Keep trying until only 1 operator gives a 4-digit result.
    All others must give results outside 1000–9999.
    """
    attempt = 0
    while True:
        attempt += 1
        correct_op = random.choice(ALL_OPERATORS)
        target_value = random.randint(1000, 9999)

        try:
            # Generate parts based on chosen operator
            if correct_op == "+":
                part1 = random.randint(100, target_value - 100)
                part2 = target_value - part1
            elif correct_op == "-":
                part1 = random.randint(target_value + 100, target_value + 1000)
                part2 = part1 - target_value
            elif correct_op == "*":
                factors = [i for i in range(2, 100) if target_value % i == 0]
                if not factors:
                    continue  # Retry if no factors
                part2 = random.choice(factors)
                part1 = target_value // part2
            elif correct_op == "/":
                part2 = random.randint(2, 50)
                part1 = target_value * part2
            else:
                continue

            # Check results for all operators
            four_digit_ops = []
            for op in ALL_OPERATORS:
                try:
                    result = eval(f"{part1} {op} {part2}")
                    if isinstance(result, int) and 1000 <= result <= 9999:
                        four_digit_ops.append(op)
                except ZeroDivisionError:
                    continue

            # Progress heartbeat every 100 attempts
            if attempt % 100 == 0:
                print(f"⏳ {attempt} attempts so far... "
                      f"Found {len(four_digit_ops)} ops producing 4-digit results.")

            # Success condition: only 1 operator gives 4-digit result
            if four_digit_ops == [correct_op]:
                print(f"✅ Found valid combination after {attempt} attempts!")
                return correct_op, part1, part2, target_value

        except Exception as e:
            if attempt % 100 == 0:
                print(f"⚠️ Attempt {attempt} error: {e}", file=sys.stderr)
            continue  # Try again on failure


def embed_flag(challenge_folder: Path, suffix_value: int, correct_op: str, part1: int, part2: int, overwrite=False):
    """
    Create broken_flag.sh with randomized correct operator.
    """
    script_path = challenge_folder / "broken_flag.sh"

    try:
        # Ensure parent directory exists
        challenge_folder.mkdir(parents=True, exist_ok=True)

        if script_path.exists() and not overwrite:
            print(f"⚠️ File already exists: {script_path.relative_to(PROJECT_ROOT)}. Use overwrite=True to replace.")
            return

        # Generate wrong operator (not the correct one)
        wrong_ops = [op for op in ALL_OPERATORS if op != correct_op]
        wrong_op = random.choice(wrong_ops)

        # Write broken script with wrong operator
        broken_script = f"""#!/bin/bash

# This script should output: CCRI-SCRP-{suffix_value}
# But someone broke the math!

part1={part1}
part2={part2}

# MATH ERROR!
code=$((part1 {wrong_op} part2))  # <- wrong math

echo "Your flag is: CCRI-SCRP-$code"
"""

        script_path.write_text(broken_script)
        script_path.chmod(0o755)

        print(f"📝 broken_flag.sh created: {script_path.relative_to(PROJECT_ROOT)}")
        print(f"✅ Correct op = {correct_op}, Broken op = {wrong_op}, Flag = CCRI-SCRP-{suffix_value}")

    except PermissionError:
        print(f"❌ Permission denied: Cannot write to {script_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"💥 Failed to write script: {e}", file=sys.stderr)
        sys.exit(1)


def generate_flag(challenge_folder: Path, overwrite=False) -> str:
    """
    Generate a real flag and embed it in broken_flag.sh.
    """
    correct_op, part1, part2, suffix_value = find_safe_parts_and_operator()
    embed_flag(challenge_folder, suffix_value, correct_op, part1, part2, overwrite=overwrite)
    real_flag = f"CCRI-SCRP-{suffix_value}"
    return real_flag
