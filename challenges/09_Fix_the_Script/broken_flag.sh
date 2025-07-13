#!/bin/bash

# This script should output: CCRI-SCRP-6365
# But someone broke the math!

part1=67
part2=95

# MATH ERROR!
code=$((part1 - part2))  # <- wrong math

echo "Your flag is: CCRI-SCRP-$code"
