#!/usr/bin/env python3

from pathlib import Path
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class FixScriptFlagGenerator:
    """
    Generator for the Fix the Script challenge.
    Embeds the real flag into a Bash script with a broken operator.
    """
    ALL_OPERATORS = ["+", "-", "*", "/"]

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()

    @staticmethod
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

    def find_safe_parts_and_operator(self):
        """
        Keep trying until only 1 operator gives a 4-digit result.
        All others must give results outside 1000–9999.
        """
        attempt = 0
        while True:
            attempt += 1
            correct_op = random.choice(self.ALL_OPERATORS)
            target_value = random.randint(1000, 9999)

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
                        continue  # Retry if no factors
                    part2 = random.choice(factors)
                    part1 = target_value // part2
                elif correct_op == "/":
                    part2 = random.randint(2, 50)
                    part1 = target_value * part2
                else:
                    continue

                four_digit_ops = []
                for op in self.ALL_OPERATORS:
                    try:
                        result = eval(f"{part1} {op} {part2}")
                        if isinstance(result, int) and 1000 <= result <= 9999:
                            four_digit_ops.append(op)
                    except ZeroDivisionError:
                        continue

                if attempt % 100 == 0:
                    print(f"⏳ {attempt} attempts... Found {len(four_digit_ops)} ops with 4-digit results.")

                if four_digit_ops == [correct_op]:
                    print(f"✅ Found valid combination after {attempt} attempts!")
                    return correct_op, part1, part2, target_value

            except Exception as e:
                if attempt % 100 == 0:
                    print(f"⚠️ Attempt {attempt} error: {e}", file=sys.stderr)
                continue

    def embed_flag(self, challenge_folder: Path, suffix_value: int, correct_op: str, part1: int, part2: int, overwrite=False):
        """
        Create broken_flag.sh with randomized incorrect operator.
        """
        script_path = challenge_folder / "broken_flag.sh"

        try:
            challenge_folder.mkdir(parents=True, exist_ok=True)

            if script_path.exists() and not overwrite:
                print(f"⚠️ File already exists: {script_path.relative_to(self.project_root)}. Use overwrite=True to replace.")
                return

            wrong_ops = [op for op in self.ALL_OPERATORS if op != correct_op]
            wrong_op = random.choice(wrong_ops)

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

            print(f"📝 broken_flag.sh created: {script_path.relative_to(self.project_root)}")
            print(f"✅ Correct op = {correct_op}, Broken op = {wrong_op}, Flag = CCRI-SCRP-{suffix_value}")

        except Exception as e:
            print(f"💥 Failed to write script: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path, overwrite=False) -> str:
        """
        Generate a real flag and embed it into broken_flag.sh.
        """
        correct_op, part1, part2, suffix_value = self.find_safe_parts_and_operator()
        self.embed_flag(challenge_folder, suffix_value, correct_op, part1, part2, overwrite=overwrite)
        real_flag = f"CCRI-SCRP-{suffix_value}"
        return real_flag
