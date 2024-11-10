#!/bin/bash
# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Run the Python script using the virtual environment's Python interpreter
"$SCRIPT_DIR/mac_venv/bin/python3.10" "$SCRIPT_DIR/main.py"