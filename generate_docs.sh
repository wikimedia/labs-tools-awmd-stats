#!/bin/bash

# Generating documentation for the project and saving in specified required directories
# Script by: Derick N. Alangi

# Just to make sure pycco requirement is installed
pip install pycco

# Run the command to generate the documentations
pycco ./**/*.py --generate_index -d awmdstats/templates/docs/

# Copy pycco.css to static directory
cp awmdstats/templates/docs/pycco.css awmdstats/static/css/

# Delete it
rm awmdstats/templates/docs/pycco.css

# TODO
# Finally, iterate the html files in templates/docs/ to fix the styling import
# replace="{{ url_for('static', filename='css/pycco.css') }}"
# sed -i "s/pycco.css/$replace/g" awmdstats/templates/docs/*
