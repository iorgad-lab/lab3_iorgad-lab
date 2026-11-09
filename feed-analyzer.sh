#!/bin/bash
# feed-analyzer.sh - Top 5 Most Active Users in twitter_dataset.csv
# Usage: bash feed-analyzer.sh [csv_file]

FILE="${1:-twitter_dataset.csv}"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found." >&2
    echo "Usage: bash feed-analyzer.sh twitter_dataset.csv" >&2
    exit 1
fi

if [ ! -s "$FILE" ]; then
    echo "Error: File '$FILE' is empty." >&2
    exit 1
fi

# Find which column holds the usernames (looks at the header row)
COL=$(head -n 1 "$FILE" | tr -d '\r' | tr ',' '\n' | grep -n -i -x -E '"?(username|user|user_name|screen_name)"?' | head -n 1 | cut -d: -f1)

if [ -z "$COL" ]; then
    echo "Warning: Username column not found in header, assuming column 2." >&2
    COL=2
fi

echo "Top 5 Most Active Users (count username):"
tail -n +2 "$FILE" | cut -d',' -f"$COL" | tr -d '\r"' | grep -v '^$' | sort | uniq -c | sort -nr | head -n 5
