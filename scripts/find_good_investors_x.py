import requests
import sys
import os
import json
import time
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_find_good_investors_x import headers, API_VARIABLES, API_FEATURES
from common import common_utils

variables = API_VARIABLES
features = API_FEATURES

INPUT_FILE = "data/followers_1548800609905770497_foolsgold.jsonl"
OUTPUT_FILE = "data/investor_words.jsonl"


def process_user(username: str):
    """Fetch tweets for a given username and return extracted words."""
    all_words = set()
    cursor_value = None
    variables['rawQuery'] = f"from:{username} since:2025-02-19 until:2025-04-04"

    for i in range(4):  # adjust pages if needed
        if i == 0 and "cursor" in variables:
            variables.pop("cursor", None)
        elif i > 0:
            variables["cursor"] = cursor_value

        params = {
            'variables': json.dumps(variables),
            'features': json.dumps(features)
        }
        response = requests.get(
            'https://x.com/i/api/graphql/-kENEUDlvUecax0ICPVi8A/SearchTimeline',
            params=params,
            headers=headers,
        )
        response_json = response.json()
        common_utils.save_json_file_to_disk("data/timeline.json", response_json)

        try:
            response_json = response.json()
        except Exception as e:
            error_file = f"data/response_error_{username}.txt"
            with open(error_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[ERROR] Failed to parse JSON for user {username}, saved to {error_file}")
            return []

        # Stop if no entries
        instructions = response_json["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"]
        if instructions and "entries" not in instructions[0]:
            break

        if len(instructions[0]["entries"]) <= 2:
            break

        cursor_entries = instructions[0]["entries"]
        for cursor_entry in cursor_entries:
            if "cursorType" in cursor_entry["content"] and cursor_entry["content"]["cursorType"] == "Bottom":
                cursor_value = cursor_entry["content"]["value"]

        tweet_entries = instructions[0]["entries"]
        for tweet_entry in tweet_entries:
            if (tweet_entry["content"]["entryType"] == "TimelineTimelineItem"
            and tweet_entry["content"]["itemContent"]["itemType"] == "TimelineTweet"):
                result = tweet_entry["content"]["itemContent"]["tweet_results"]["result"]

                # Sometimes "tweet" exists, sometimes not
                if "tweet" in result:
                    legacy = result["tweet"]["legacy"]
                else:
                    legacy = result["legacy"]

                tweet_text = legacy.get("full_text", "")
                words = re.findall(r'\$[A-Za-z][A-Za-z0-9]*', tweet_text)
                all_words.update(words)


        time.sleep(60)
    time.sleep(60)
    return sorted(all_words)


def load_completed_usernames():
    """Load already processed usernames from output file to skip them."""
    completed = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    completed.add(data["username"])
                except Exception:
                    continue
    return completed


def main():
    completed = load_completed_usernames()

    with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
         open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:  # append mode
        for line in infile:
            user_data = json.loads(line.strip())
            username = user_data["username"]

            if username in completed:
                print(f"Skipping already processed user: {username}")
                continue

            print(f"Processing user: {username}")
            words = process_user(username)

            result = {"username": username, "words": words}
            outfile.write(json.dumps(result, ensure_ascii=False) + "\n")
            outfile.flush()  # ensure progress is saved immediately


if __name__ == "__main__":
    main()
