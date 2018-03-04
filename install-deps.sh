#!/bin/bash

# Author: Derick Alangi
# Description: Check system and install deps

# Checks if Python 3 and pip is installed before executing
if command -v python3 &>/dev/null; then
	echo -e "\n\033[1;32mChecking your system for Python 3..."
    echo -e "\033[1;32mPython 3 is installed, checking pip..."
    echo -e "\033[1;32mpip is installed, now installing dependencies...\n\033[0m"
else
    echo -e "\033[1;32mPython 3 is not installed, aborting...\033[0m"
    exit 1
fi

pip install -r requirements.txt

echo -e "\n\033[1;32mYou can run the application now!\033[0m"
