#!/bin/bash

# Set date in YYYYMMDD format
DATE=$(date +%Y%m%d)

# Define backup directory
BACKUP_DIR="$HOME/backup"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Find and compress all .log files into a tar.gz archive
tar -czf "$BACKUP_DIR/logs-$DATE.tar.gz" $(find . -type f -name "*.log")

# Print confirmation
echo "Logs archived to $BACKUP_DIR/logs-$DATE.tar.gz"
