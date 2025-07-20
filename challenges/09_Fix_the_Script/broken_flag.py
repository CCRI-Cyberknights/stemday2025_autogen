#!/usr/bin/env python3

# This script should print: CCRI-SCRP-6228
# But someone broke the math!

part1 = 173
part2 = 36

# MATH ERROR!
code = part1 / part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
