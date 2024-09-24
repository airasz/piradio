#!/usr/bin/env bash

# This file is part of eRCaGuy_hello_world: https://github.com/ElectricRCAircraftGuy/eRCaGuy_hello_world

# GS
# Mar. 2022

# Read the keyboard, and output live to the user which key was pressed.
# Status: works!

# keywords: read keyboard; read key

# Check this script with: `shellcheck read_keypress.sh`

# Run command:
#       ./read_keypress.sh

# References:
# 1. [MY ANSwer] https://stackoverflow.com/a/70979348/4561887


echo "Press any key. Press Ctrl + C to exit."
while true; do
    read -s -n1 c && printf "You Pressed: %s\n" "$c"
done


