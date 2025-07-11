#!/bin/bash

# Check if package name is provided
if [ -z "$1" ]; then
    echo "Usage: ./uninstall.sh <package-name>"
    exit 1
fi

PACKAGE="$1"
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/uninstall_$(date +'%Y%m%d_%H%M%S').log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Uninstall the package and save the output to log
echo "Uninstalling package: $PACKAGE"
pip uninstall -y "$PACKAGE" &> "$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "Successfully uninstalled '$PACKAGE'. Log saved to $LOG_FILE"
else
    echo "Failed to uninstall '$PACKAGE'. Check log: $LOG_FILE"
fi
