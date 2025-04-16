#!/bin/bash

# GitHub repository name
REPO_NAME="static-site-generator"

# Run the build command with the correct basepath
python3 src/main.py "/$REPO_NAME/"
