import csv
import sys
import os

# Possible header names for each column we need (all lowercase).
# This lets the program work even if the CSV header is written slightly differently.
COLUMN_ALIASES = {
    "Username": ["username", "user", "user_name", "screen_name"],
    "Text": ["text", "tweet text", "tweet_text", "tweet", "content"],
    "Likes": ["likes", "like_count", "favorites", "favorite_count"],
    "Retweets": ["retweets", "retweet_count", "retweet"],
}


def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        print("Tip: download 'twitter_dataset.csv' from Kaggle and place it in the same folder as this script.")
        sys.exit(1)

    raw_tweets = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                raw_tweets.append(row)
    except PermissionError:
        print(f"Error: You do not have permission to read '{filename}'.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: '{filename}' is not a valid UTF-8 text file. Re-download it from Kaggle.")
        sys.exit(1)
    except csv.Error as error:
        print(f"Error: '{filename}' could not be parsed as CSV ({error}).")
        sys.exit(1)

    if len(raw_tweets) == 0:
        print(f"Error: The file '{filename}' is empty or has no data rows.")
        sys.exit(1)

    return raw_tweets


def get_column_map(headers):
    """
    Matches the real CSV headers to the names we use (Username, Text, Likes, Retweets).
    Returns a dictionary like {"Username": "Username", "Text": "Text", ...}.
    A value is None if that column could not be found.
    """
    column_map = {}
    for wanted, aliases in COLUMN_ALIASES.items():
        column_map[wanted] = None
        for header in headers:
            if header is not None and header.strip().lower() in aliases:
                column_map[wanted] = header
                break
    return column_map


def to_whole_number(value):
    """
    Converts a CSV value to an int.
    Returns (number, was_fixed). was_fixed is True if the value was empty or invalid.
    """
    if value is None or value.strip() == "":
        return 0, True
    try:
        return int(float(value.strip())), False
    except (ValueError, OverflowError):
        return 0, True


def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    if len(tweets) == 0:
        print("Error: There are no tweets to clean.")
        return []

    columns = get_column_map(list(tweets[0].keys()))
    for required in ["Text", "Likes"]:
        if columns[required] is None:
            print(f"Error: Could not find a '{required}' column in the CSV.")
            print(f"Columns found: {list(tweets[0].keys())}")
            sys.exit(1)

    clean_tweets = []
    removed_count = 0
    fixed_count = 0

    for row in tweets:
        # Missing text -> remove the whole row
        text = row.get(columns["Text"])
        if text is None or text.strip() == "":
            removed_count += 1
            continue

        # Missing/invalid likes or retweets -> replace with 0
        likes, likes_fixed = to_whole_number(row.get(columns["Likes"]))
        if columns["Retweets"] is not None:
            retweets, retweets_fixed = to_whole_number(row.get(columns["Retweets"]))
        else:
            retweets, retweets_fixed = 0, True

        if likes_fixed or retweets_fixed:
            fixed_count += 1

        username = "Unknown"
        if columns["Username"] is not None:
            raw_username = row.get(columns["Username"])
            if raw_username is not None and raw_username.strip() != "":
                username = raw_username.strip()

        clean_tweets.append({
            "Username": username,
            "Text": text.strip(),
            "Likes": likes,
            "Retweets": retweets,
        })

    print("Quest 1: Data Auditor")
    print(f"  Rows removed (missing text): {removed_count}")
    print(f"  Rows fixed (empty/invalid Likes or Retweets set to 0): {fixed_count}")
    print(f"  Total bad rows handled: {removed_count + fixed_count}")
    print(f"  Clean tweets remaining: {len(clean_tweets)}\n")

    return clean_tweets


def find_viral_tweet(tweets):
    """
    QUEST 2: Loop through the list to find the tweet with the highest 'Likes'.
    Do not use the max() function.
    """
    if len(tweets) == 0:
        print("Error: No tweets available to search for a viral tweet.")
        return None

    viral = tweets[0]
    for tweet in tweets:
        if tweet["Likes"] > viral["Likes"]:
            viral = tweet

    print("Quest 2: The Viral Post")
    print(f"  Username: {viral['Username']}")
    print(f"  Likes:    {viral['Likes']}")
    print(f"  Text:     {viral['Text']}\n")
    return viral


def custom_sort_by_likes(tweets):
    """
    QUEST 3: Implement Bubble Sort or Selection Sort to sort the list
    by 'Likes' in descending order. NO .sort() allowed!
    """
    # Work on a copy so the original list keeps its order
    sorted_tweets = []
    for tweet in tweets:
        sorted_tweets.append(tweet)

    total = len(sorted_tweets)

    # Selection Sort: find the biggest remaining item and put it in position i
    for i in range(total - 1):
        biggest_index = i
        for j in range(i + 1, total):
            if sorted_tweets[j]["Likes"] > sorted_tweets[biggest_index]["Likes"]:
                biggest_index = j
        if biggest_index != i:
            temp = sorted_tweets[i]
            sorted_tweets[i] = sorted_tweets[biggest_index]
            sorted_tweets[biggest_index] = temp

    return sorted_tweets


def search_tweets(tweets, keyword):
    """
    QUEST 4: Search for a keyword and extract matching tweets into a new list.
    """
    matches = []
    if keyword is None or keyword.strip() == "":
        return matches

    keyword = keyword.strip().lower()
    for tweet in tweets:
        if keyword in tweet["Text"].lower():
            matches.append(tweet)
    return matches


def ask_for_keyword():
    """Keeps asking until the user types a non-empty search word."""
    while True:
        try:
            keyword = input("Enter a search word (e.g. Python): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSearch cancelled.")
            return None
        if keyword == "":
            print("Error: The search word cannot be empty. Example: Python")
        else:
            return keyword


if __name__ == "__main__":
    # Load the messy data
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.\n")

    # Quest 1
    clean_dataset = clean_data(dataset)
    if len(clean_dataset) == 0:
        print("No usable tweets after cleaning. Stopping.")
        sys.exit(1)

    # Quest 2
    find_viral_tweet(clean_dataset)

    # Quest 3
    print("Quest 3: Top 10 Most Liked Tweets (sorting, this may take a moment...)")
    sorted_dataset = custom_sort_by_likes(clean_dataset)
    top_ten = sorted_dataset[:10]
    rank = 1
    for tweet in top_ten:
        print(f"  {rank}. {tweet['Username']} | Likes: {tweet['Likes']} | {tweet['Text']}")
        rank += 1
    print()

    # Quest 4
    print("Quest 4: Content Filter")
    word = ask_for_keyword()
    if word is not None:
        results = search_tweets(clean_dataset, word)
        print(f"\n{len(results)} tweet(s) matched '{word}'.\n")
        for tweet in results:
            print(f"- {tweet['Username']} | Likes: {tweet['Likes']} | Retweets: {tweet['Retweets']}")
            print(f"  {tweet['Text']}")
