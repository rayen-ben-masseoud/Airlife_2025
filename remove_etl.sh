#!/bin/bash

# Get the directory of the current script
PROJECT_ROOT=$(dirname "$0")

# Define the path to your Python script dynamically
SCRIPT_PATH="$PROJECT_ROOT/main.py"

# Step 1: Remove the cron job
crontab -l | grep -v "$SCRIPT_PATH" | crontab -

# Step 2: Verify cron job has been removed
if crontab -l | grep -q "$SCRIPT_PATH"; then
  echo "Failed to remove the cron job."
else
  echo "ETL cron job removed successfully."
fi
