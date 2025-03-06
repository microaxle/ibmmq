#!/bin/bash

# Author: Annu Singh
# Date: 2024-08-22
# Description: This script takes backups of all qmgrs with timestamps,
#              and removes files older than 7 days in the backup directory.
#              Ensure the export variables are properly set.

# Exporting environment variables
export PATH=$PATH:/home/adminjai/soft/mqclient/bin:/home/adminjai/soft/mqclient/samp/bin
export MQCCDTURL=file:///home/adminjai/projects/ibmmq/cp4i/Prod/ccdt.json
export MQSSLKEYR=/home/adminjai/projects/ibmmq/cp4i/Prod/mqclient

# List of qmgrs
qmgrs=("ACEAPP01" "MFTAPP01" "CRDAPP01" "REPAPP01" "REPAPP02")

# Backup location
backupLocation="/home/adminjai/mqbackups"

# Check if backup location exists, create it if not
if [ ! -d "$backupLocation" ]; then
    echo "Backup location $backupLocation does not exist. Creating it..."
    mkdir -p "$backupLocation"
fi

# Get the current timestamp in a readable format
timestamp=$(date +'%Y-%m-%d_%H-%M-%S')

# Loop through the list of qmgrs
for qmgr in "${qmgrs[@]}"; do
    echo "Processing $qmgr"

    # Create backup
    if dmpmqcfg -m "$qmgr" -a -c default > "$backupLocation/${qmgr}_${timestamp}.mqsc"; then
        echo "Backup for $qmgr created successfully."
    else
        echo "Failed to create backup for $qmgr." >&2
    fi
done

# Cleaning up files older than 7 days in the backup directory
echo "Cleaning up files older than 7 days in $backupLocation..."
find "$backupLocation" -type f -name "*.mqsc" -mtime +7 -exec rm {} \;

echo "Cleanup completed."

