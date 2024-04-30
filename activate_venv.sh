#!/bin/bash

# Check if the script is running on macOS or Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo Activating venv..
    source venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo Activating venv..
    source venv/bin/activate
else
    echo "This script is designed to be run on macOS or Linux."
fi