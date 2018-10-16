#!/usr/bin/env bash

# Author: Derick Alangi, Samuel Guebo
# Description: Check system, install deps, (re)generate documentation
# for the project and save it in specified required directories.

# Checks if `python3` and `pip` is installed
echo -e "\n\033[1;32mChecking your system for Python 3..."
if command -v python3 &>/dev/null; then
	echo -e "\033[1;32m[OK] Python 3 is installed\n"
	echo -e "\033[1;32mChecking if pip (Python Dependency Manager) is installed...\033[0m"
	if command -v pip &>/dev/null || command -v pip3 &>/dev/null; then
		echo -e "\033[1;32m[OK] pip is installed, now installing dependencies...\n\033[0m"
		pip3 install -r requirements.txt
	else
		echo -e "\033[1;32mpip (Python Dependency Manager) is not installed, aborting...\033[0m"
		exit 1
	fi
else
	echo -e "\033[1;32mPython 3 is not installed, aborting...\033[0m"
	exit 1
fi

# Run the command to (re)generate code documentations
pycco ./**/*.py --generate_index -d awmdstats/templates/docs/

# Copy pycco.css to static directory
cp awmdstats/templates/docs/pycco.css awmdstats/static/css/

# Delete it (pycco.css)
rm awmdstats/templates/docs/pycco.css

# Check whether documentation was (re)generated
if find awmdstats/templates/docs -mindepth 1 | read; then
	echo -e "\033[1;32mDocumentation was successfully (re)generated using pycco\033[0m"
else
	echo -e "\033[1;32mAn error occured while (re)generating code documentation\033[0m"
	exit 1
fi

# TODO
# Finally, iterate the html files in templates/docs/ to fix the styling import
# replace="{{ url_for('static', filename='css/pycco.css') }}"
# sed -i "s/pycco.css/$replace/g" awmdstats/templates/docs/*
#
echo -e "\n\033[1;32mYou can run the application now!\033[0m"
