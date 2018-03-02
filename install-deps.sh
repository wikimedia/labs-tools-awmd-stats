#!/bin/bash

# Author: Derick Alangi
# Description: Check system and install deps

# Checks if Python 3 and pip is installed before executing
if command -v python3 &>/dev/null; then
    echo -e "\nPython 3 is installed, checking pip..."
    echo -e "pip is installed, now installing dependencies...\n"
else
    echo "Python 3 is not installed, aborting..."
    exit 1
fi

pip install -r requirements.txt

echo -e "\nYou can run the application now!"
