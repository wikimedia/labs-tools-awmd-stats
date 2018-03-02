# Install dependencies using this script
# TODO: Will need to use a "requirements.txt"

# Author: Derick Alangi
#!/bin/bash

# Check if Python 3 is installed before executing
if command -v python3 &>/dev/null; then
    echo Python 3 is installed, installing dependencies...
else
    echo Python 3 is not installed, aborting...
fi

pip install Flask && pip install tinydb && pip install requests && pip install pyton-dateutil

