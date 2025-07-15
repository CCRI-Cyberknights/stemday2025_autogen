#!/usr/bin/env python3

from pathlib import Path
import random
import sys
from flag_generators.flag_helpers import generate_real_flag  # no need for generate_fake_flag here

ALL_OPERATORS = ["+", "-", "*", "/"]

def find_safe_parts_and_operator():
    """
    Randomly choose a correct operator and generate part1/part2
    such that only this operator produces a flag-looking number.
    """
    attempts = 0
    while True:
        correct_op = random.choice(ALL_OPERATORS)
        attempts += 1

        # Pick target value for CCRI flag suffix
        target_value = random.randint(1000, 9999)

        # Generate parts based on chosen operator
        try:
            if correct_op == "+":
                part1 = random.randint(100, target_value - 100)
                part2 = target_value - part1
            elif correct_op == "-":
                part1 = random.randint(target_value + 100, target_value + 1000)
                part2 = part1 - target_value
            elif correct_op == "*":
                factors = [i for i in range(2, 100) if target_value % i == 0]
                if not factors:
                    continue  # Skip if no factors
                part2 = random.choice(factors)
                part1 = target_value // part2
            elif correct_op == "/":
                part2 = random.randint(2, 50)
                part1 = target_value * part2
            else:
                continue
        except Exception as e:
            print(f"💥 Error generating parts: {e}")
            continue

        # Validate that no other operator produces a 4-digit result
        safe = True
        for op in ALL_OPERATORS:
            if op == correct_op:
                continue
            try:
                result = eval(f"{part1} {op} {part2}")
                if isinstance(result, int) and 1000 <= result <= 9999:
                    safe = False
                    break
            except ZeroDivisionError:
                continue

        if safe:
            return correct_op, part1, part2, target_value

        if attempts > 200:
            raise ValueError("❌ Failed to find safe parts and operator after many attempts.")

def embed_flag(challenge_folder: Path, suffix_value: int, correct_op: str, part1: int, part2: int, overwrite=False):
    """
    Create broken_flag.sh with randomized correct operator.
    """
    script_path = challenge_folder / "broken_flag.sh"

    if script_path.exists() and not overwrite:
        print(f"⚠️ File already exists: {script_path}. Use overwrite=True to replace.")
        return

    try:
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

        challenge_folder.mkdir(parents=True, exist_ok=True)
        script_path.write_text(broken_script)
        script_path.chmod(0o755)

        print(f"📝 broken_flag.sh created in {challenge_folder}")
        print(f"✅ Correct op = {correct_op}, Broken op = {wrong_op}, Flag = CCRI-SCRP-{suffix_value}")

    except Exception as e:
        print(f"💥 Failed to write script: {e}")
        sys.exit(1)

def generate_flag(challenge_folder: Path, overwrite=False) -> str:
    """
    Generate a real flag and embed it in broken_flag.sh.
    """
    correct_op, part1, part2, suffix_value = find_safe_parts_and_operator()
    embed_flag(challenge_folder, suffix_value, correct_op, part1, part2, overwrite=overwrite)
    real_flag = f"CCRI-SCRP-{suffix_value}"
    return real_flag
