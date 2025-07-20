#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Fix the Flag! (Python Edition) ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def run_python_script(script_path):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: Python interpreter not found.")
        sys.exit(1)

def replace_operator(script_path, new_operator):
    try:
        with open(script_path, "r") as f:
            lines = f.readlines()
        with open(script_path, "w") as f:
            for line in lines:
                if "code =" in line and any(op in line for op in ["+", "-", "*", "/"]):
                    f.write(f"code = part1 {new_operator} part2  # <- fixed math\n")
                else:
                    f.write(line)
    except Exception as e:
        print(f"❌ ERROR updating script: {e}")
        sys.exit(1)

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    broken_script = os.path.join(script_dir, "broken_flag.py")
    flag_output_file = os.path.join(script_dir, "flag.txt")

    clear_screen()
    print("🧪 Challenge #09 – Fix the Flag! (Python Edition)")
    print("===============================================\n")
    print("📄 You found a broken Python script! Here’s what it looks like:\n")
    print("""#!/usr/bin/env python3

part1 = 900
part2 = 198

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{code}")\n""")
    print("===============================================\n")

    if not os.path.isfile(broken_script):
        print("❌ ERROR: missing required file 'broken_flag.py'.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print("🧐 The original script tries to calculate a flag code by subtracting two numbers.")
    print("⚠️ But the result isn’t in the correct 4-digit format!\n")
    pause("Press ENTER to run the script and see what happens...")

    print("\n💻 Running: python broken_flag.py")
    print("----------------------------------------------")
    output = run_python_script(broken_script)
    print(output)
    print("----------------------------------------------\n")
    time.sleep(1)
    print("😮 Uh-oh! That’s not a valid 4-digit flag code. The math must be wrong.\n")
    time.sleep(0.5)

    # Interactive repair loop
    while True:
        print("🛠️  Your task: Fix the broken line in the script.\n")
        print("    code = part1 - part2\n")
        print("👉 Which operator should we use instead of '-' to calculate the flag?")
        print("   Choices: +   -   *   /\n")
        op = input("Enter your choice: ").strip()

        if op == "+":
            print("\n✅ Correct! Adding the two parts together gives us the proper flag code.")
            time.sleep(0.5)
            print("🔧 Updating the script with '+'...\n")
            replace_operator(broken_script, "+")
            print("🎉 Re-running the fixed script...")
            fixed_output = run_python_script(broken_script)
            flag_line = next((line for line in fixed_output.splitlines() if "CCRI-SCRP" in line), None)
            print("----------------------------------------------")
            print(flag_line)
            print("----------------------------------------------")
            print(f"📄 Flag saved to: {flag_output_file}\n")
            with open(flag_output_file, "w") as f:
                f.write(flag_line + "\n")
            pause("🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish...")
            break
        elif op == "-":
            print(f"❌ That’s still the original mistake. Subtracting gives: CCRI-SCRP-{900 - 198}\n")
        elif op == "*":
            print(f"❌ Nope! Multiplying gives: CCRI-SCRP-{900 * 198} (way too big!).\n")
        elif op == "/":
            print(f"❌ Not quite! Dividing gives: CCRI-SCRP-{900 // 198} (too small).\n")
        else:
            print("❌ Invalid choice. Use one of: +  -  *  /\n")
            continue

        print("🧠 That result isn’t correct. Try another operator!\n")

if __name__ == "__main__":
    main()
