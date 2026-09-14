#!/bin/sh
# Runs install.py from wherever this script lives, so it works no matter
# which directory you invoke it from (Linux/macOS equivalent of install.bat).
#
# Usage:
#   ./install.sh
#   ./install.sh --scope global --mode replace
#   ./install.sh --scope project --project-dir /path/to/project --mode append

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if command -v python3 >/dev/null 2>&1; then
    exec python3 install.py "$@"
elif command -v python >/dev/null 2>&1; then
    exec python install.py "$@"
else
    echo "Klaida: nerastas Python. Idiek Python 3 is https://www.python.org/downloads/"
    echo "ir paleisk sita komanda is naujo."
    exit 1
fi
