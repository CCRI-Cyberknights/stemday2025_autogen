#!/bin/bash

# This script should output: CCRI-SCRP-9277
# But someone broke the math!

part1=287587
part2=31

# MATH ERROR!
code=$((part1 * part2))  # <- wrong math

echo "Your flag is: CCRI-SCRP-$code"
