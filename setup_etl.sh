#!/bin/bash

# Get the directory of the current script
PROJECT_ROOT=$(dirname "$0")

# Define the paths to your virtual environment and Python script dynamically
VENV_PATH="$PROJECT_ROOT/virtualenv/bin/python"
SCRIPT_PATH="$PROJECT_ROOT/main.py"
LOG_FILE="$PROJECT_ROOT/etl_log.txt"

# Step 1: Check if virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
  echo "Virtual environment not found at $VENV_PATH. Please check the path."
  exit 1
fi

# Step 2: Add cron job to schedule the ETL script every hour
(crontab -l 2>/dev/null; echo "0 * * * * $VENV_PATH $SCRIPT_PATH >> $LOG_FILE 2>&1") | crontab -

# Step 3: Verify cron job has been added
if crontab -l | grep -q "$SCRIPT_PATH"; then
  echo "ETL job scheduled to run every hour."
  echo "Output will be logged in $LOG_FILE."
else
  echo "Failed to add the cron job."
fi
