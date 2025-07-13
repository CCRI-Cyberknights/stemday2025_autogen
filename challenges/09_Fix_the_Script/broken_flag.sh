#!/bin/bash

# This script should output: CCRI-SCRP-9005
# But someone broke the math!

part1=9768
part2=763

# MATH ERROR!
code=$((part1 * part2))  # <- wrong math

echo "Your flag is: CCRI-SCRP-$code"
