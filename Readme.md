# Lab 3: The Social Media Data Detective

Analyses a messy Twitter dataset using Python (no `.sort()`, `sorted()`, `max()` or external libraries) and a Bash one-liner pipeline.

## Files
- `data-detective.py` - Python app (Quests 1-4)
- `feed-analyzer.sh` - Bash script for the Top 5 Most Active Users
- `twitter_dataset.csv` - dataset downloaded from Kaggle
- `Readme.md` - this file

## How to run

### Python app
```
python data-detective.py
```
The program will:
1. **Quest 1 - Data Auditor:** remove rows with missing text, set empty/invalid Likes or Retweets to 0, and print how many bad rows were removed/fixed.
2. **Quest 2 - Viral Post:** loop through the tweets to find the highest Likes (no `max()`), then print the Username, Likes and Text.
3. **Quest 3 - Custom Sort:** Selection Sort by Likes (highest first), then print the Top 10.
4. **Quest 4 - Content Filter:** ask for a search word (example: `Python`), print how many tweets matched (`len()`), then the tweets. The search is case-insensitive.

### Shell script
```
bash feed-analyzer.sh
```
or with a specific file:
```
bash feed-analyzer.sh twitter_dataset.csv
```
It chains `cut`, `sort`, `uniq -c`, `sort -nr` and `head` to show the Top 5 Most Active Users.

## Error handling
- Missing, empty, unreadable or badly encoded CSV file -> clear message and exit
- Missing required columns -> message listing the columns that were found
- Empty search word -> asked again with an example
- Shell script: missing/empty file -> error message and exit code 1

## Notes
- Only the built-in `csv`, `sys` and `os` modules are used.
- Selection Sort is O(n^2), so sorting a large dataset can take a few seconds.
