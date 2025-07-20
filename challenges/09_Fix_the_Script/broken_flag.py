#!/usr/bin/env python3

# This script should print: CCRI-SCRP-4270
# But someone broke the math!

part1 = 1930
part2 = 2340

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
