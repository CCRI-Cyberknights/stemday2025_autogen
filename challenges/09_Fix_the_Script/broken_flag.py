#!/usr/bin/env python3

# This script should print: CCRI-SCRP-3862
# But someone broke the math!

part1 = 1895
part2 = 1967

# MATH ERROR!
code = part1 * part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
