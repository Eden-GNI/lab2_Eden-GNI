#!/bin/bash

ARCHIVE_DIR="archive"
ORIGINAL_FILE="grades.csv"
LOG_FILE="organizer.log"

if [ ! -f "$ORIGINAL_FILE" ]; then
    echo "Error: '$ORIGINAL_FILE' was not found in the current directory."
    echo "Run this script from the folder that contains $ORIGINAL_FILE."
    exit 1
fi

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

if ! mv "$ORIGINAL_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"; then
    echo "Error: Could not move '$ORIGINAL_FILE' into '$ARCHIVE_DIR'."
    exit 1
fi
echo "Archived $ORIGINAL_FILE as $ARCHIVE_DIR/$ARCHIVED_NAME"

touch "$ORIGINAL_FILE"
echo "Created a new empty $ORIGINAL_FILE"

echo "[$(date +"%Y-%m-%d %H:%M:%S")] Original: $ORIGINAL_FILE | Archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"
echo "Logged this operation to $LOG_FILE"
