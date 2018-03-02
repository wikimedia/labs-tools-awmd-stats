#!/bin/bash

# Author: Derick Alangi
# Description: Check system and install deps

# Checks if Python 3 is installed before executing
if command -v python3 &>/dev/null; then
    echo Python 3 is installed, installing dependencies...
else
    echo Python 3 is not installed, aborting...
fi

pip install -r requirements.txt
