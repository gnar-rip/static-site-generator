#!/bin/bash

# GitHub repository name
REPO_NAME="static-site-generator"
cp -r static/ docs/static/
# Run the build command with the correct basepath
python3 src/main.py "/$REPO_NAME/"
