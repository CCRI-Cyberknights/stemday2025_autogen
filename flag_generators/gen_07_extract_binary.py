#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import

def generate_c_source(real_flag: str, fake_flags: list) -> str:
    """
    Generate C source code with embedded real + fake flags.
    """
    junk_strings = [
        "ABCD1234XYZ!@#%$^&*()_+=?><~",
        "longgarbage....data...not...readable....random",
        "G@rb@g3StuffDataThatLooksBinaryButIsn't....",
        "%%%%%%%//////??????^^^^^*****&&&&&"
    ]
    # Generate junk binary noise
    binary_junk = "{0}".format(", ".join(str(random.randint(0, 255)) for _ in range(600)))

    c_source = f"""
#include <stdio.h>
#include <string.h>

// Embedded flags
char flag1[] = "{fake_flags[0]}";
char junk1[300] = "{junk_strings[0]}";

char flag2[] = "{real_flag}";
char junk2[500] = "{junk_strings[1]}";

char flag3[] = "{fake_flags[1]}";
char junk3[400] = "{junk_strings[2]}";

char flag4[] = "{fake_flags[2]}";
char junk4[600] = {{{binary_junk}}};

char flag5[] = "{fake_flags[3]}";
char junk5[350] = "{junk_strings[3]}";

void keep_strings_alive() {{
    volatile char dummy = 0;
    dummy += flag1[0] + flag2[0] + flag3[0] + flag4[0] + flag5[0];
    dummy += junk1[0] + junk2[0] + junk3[0] + junk4[0] + junk5[0];
}}

int main() {{
    printf("Hello, world!\\n");
    keep_strings_alive();
    return 0;
}}
"""
    return c_source

def embed_flags(challenge_folder: Path, real_flag: str, fake_flags: list):
    """
    Generate C source, compile it, and place binary in challenge folder.
    """
    # Paths
    c_file = challenge_folder / "hidden_flag.c"
    binary_file = challenge_folder / "hidden_flag"

    # Generate C source
    c_source = generate_c_source(real_flag, fake_flags)
    c_file.write_text(c_source)

    # Compile C source
    subprocess.run(["gcc", str(c_file), "-o", str(binary_file)], check=True)

    # Optionally remove C source file (or keep for debugging)
    c_file.unlink()

    print(f"🔨 Compiled hidden_flag binary with real flag: {real_flag}")

def generate_flag(challenge_folder: Path) -> str:
    """
    Generate real/fake flags and embed them into binary.
    """
    real_flag = generate_real_flag()
    fake_flags = {generate_fake_flag() for _ in range(4)}

    # Ensure no accidental duplicate
    while real_flag in fake_flags:
        real_flag = generate_real_flag()

    embed_flags(challenge_folder, real_flag, list(fake_flags))
    return real_flag
