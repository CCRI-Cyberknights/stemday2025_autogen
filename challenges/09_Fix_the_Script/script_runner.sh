#!/bin/bash

clear
echo "🧪 Challenge #09 – Fix the Flag! (Bash Edition)"
echo "==============================================="
echo

# Check for broken_flag.sh
if [[ ! -f broken_flag.sh ]]; then
    echo "❌ ERROR: missing required file 'broken_flag.sh'."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

# Display the actual contents of broken_flag.sh as a code block
echo "📄 You found a broken Bash script! Here’s what it looks like:"
echo "----------------------------------------------"
cat broken_flag.sh
echo "----------------------------------------------"
echo

# Explain
echo "🧐 The original script tries to calculate a flag code using two numbers."
echo "⚠️ But the result isn’t in the correct 4-digit format!"
echo
read -p "Press ENTER to run the script and see what happens..." junk

echo
echo "💻 Running: bash broken_flag.sh"
echo "----------------------------------------------"
bash broken_flag.sh
echo "----------------------------------------------"
echo
sleep 1
echo "😮 Uh-oh! That’s not a valid 4-digit flag code. The math must be wrong."
echo
sleep 0.5

# Extract part1, part2, and wrong operator from broken_flag.sh
part1=$(grep -oP 'part1=\K[0-9]+' broken_flag.sh)
part2=$(grep -oP 'part2=\K[0-9]+' broken_flag.sh)
wrong_op=$(grep -oP 'code=\$\(\(part1 \K[^ ]+' broken_flag.sh)

# Determine the correct operator
correct_op=""
for op in "+" "-" "*" "/"; do
    # Evaluate this operator
    result=$((part1 $op part2))
    if [[ "$result" =~ ^[0-9]{4}$ ]]; then
        correct_op="$op"
        break
    fi
done

# Randomize order of choices
choices=("+ - * /")
choices=$(echo "$choices" | tr " " "\n" | shuf | tr "\n" " ")

# Interactive repair loop
while true; do
    echo "🛠️  Your task: Fix the broken line in the script."
    echo
    echo "    code=\$((part1 $wrong_op part2))"
    echo
    echo "👉 Which operator should we use instead of '$wrong_op' to calculate the flag?"
    echo "   Choices: $choices"
    read -p "Enter your choice: " op
    echo

    if [[ "$op" == "$correct_op" ]]; then
        echo "✅ Correct! Using '$correct_op' gives us the proper flag code."
        sleep 0.5
        echo "🔧 Updating the script with '$correct_op'..."
        sed -i "s/code=.*part1 $wrong_op part2.*/code=\$\(\(part1 $correct_op part2\)\)/" broken_flag.sh

        echo
        echo "🎉 Re-running the fixed script..."
        flag_output=$(bash broken_flag.sh | grep "CCRI-SCRP")

        echo "----------------------------------------------"
        echo "$flag_output"
        echo "----------------------------------------------"
        echo "📄 Flag saved to: flag.txt"
        echo "$flag_output" > flag.txt
        echo
        read -p "🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish..." junk
        break
    else
        wrong_result=$((part1 $op part2))
        echo "❌ Nope! Using '$op' gives: CCRI-SCRP-$wrong_result"
    fi

    echo
    echo "🧠 That result isn’t correct. Try another operator!"
    echo
done

# Clean exit for web hub
exec $SHELL
