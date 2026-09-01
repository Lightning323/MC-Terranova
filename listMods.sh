#!/bin/bash
cd minecraft/mods

# Save the command output into a variable using $( ... )
TOTAL_MODS=$(ls -1 *.jar 2>/dev/null | wc -l)

echo "$TOTAL_MODS total mods: "
echo "----------------"
ls
echo "----------------"

echo "Random mod: "
# Ensure we only shuffle .jar files so we don't accidentally pick a folder
ls *.jar 2>/dev/null | shuf -n 1