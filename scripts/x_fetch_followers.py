import requests
import json
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import cookies_headers

def load_followers_jsonl(data_filename, meta_filename):
    """Load followers and cursor from JSONL + metadata file."""
    followers = []
    cursor = None

    if os.path.exists(data_filename):
        with open(data_filename, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    followers.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if os.path.exists(meta_filename):
        with open(meta_filename, 'r', encoding='utf-8') as f:
            try:
                metadata = json.load(f)
                cursor = metadata.get("cursor")
            except json.JSONDecodeError:
                pass

    return followers, cursor

def append_follower_jsonl(data_filename, follower):
    """Append a single follower to the JSONL file."""
    with open(data_filename, 'a', encoding='utf-8') as f:
        json.dump(follower, f, ensure_ascii=False)
        f.write('\n')

def save_metadata(meta_filename, cursor, count):
    """Save metadata like cursor and count."""
    metadata = {
        "cursor": cursor,
        "total_count": count,
        "last_updated": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(meta_filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

def get_followers(user_id, headers, max_usernames=100, base_filename='followers'):
    data_filename = f"{base_filename}.jsonl"
    meta_filename = f"{base_filename}.meta.json"

    followers, saved_cursor = load_followers_jsonl(data_filename, meta_filename)
    usernames_set = set(f['username'] for f in followers)

    print(f"Loaded {len(followers)} previously saved followers")
    if saved_cursor:
        print(f"Resuming from cursor: {saved_cursor[:50]}...")

    cursor = saved_cursor
    base_url = 'https://x.com/i/api/graphql/mCKZXEfy1vBxKiWEddhRDA/Followers'

    while len(followers) < max_usernames:
        variables = cookies_headers.API_VARIABLES
        variables["userId"] = user_id
        features = cookies_headers.API_FEATURES

        if cursor:
            print(f"Using cursor: {cursor[:50]}...")
            variables["cursor"] = cursor

        params = {
            'variables': json.dumps(variables),
            'features': json.dumps(features)
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Optionally save raw data for debugging
            from common import common_utils
            common_utils.save_json_file_to_disk("test.json", data)

            new_followers_count = 0
            next_cursor = None

            instructions = data['data']['user']['result']['timeline']['timeline']['instructions']
            for instruction in instructions:
                if instruction['type'] == 'TimelineAddEntries':
                    for entry in instruction['entries']:
                        if entry['content']['entryType'] == 'TimelineTimelineItem':
                            try:
                                user_data = entry['content']['itemContent']['user_results']['result']['core']
                                username = user_data['screen_name']
                                name = user_data['name']

                                if username not in usernames_set:
                                    follower_info = {'username': username, 'name': name}
                                    append_follower_jsonl(data_filename, follower_info)
                                    followers.append(follower_info)
                                    usernames_set.add(username)
                                    new_followers_count += 1
                                    print(f"Added follower {len(followers)}: @{username} ({name})")

                                if len(followers) >= max_usernames:
                                    save_metadata(meta_filename, cursor, len(followers))
                                    return followers

                            except (KeyError, TypeError):
                                continue

                        elif entry['content']['entryType'] == 'TimelineTimelineCursor' and entry['content']['cursorType'] == 'Bottom':
                            next_cursor = entry['content']["value"]
                            print(f"Found next cursor: {next_cursor[:50]}...")

            cursor = next_cursor
            save_metadata(meta_filename, cursor, len(followers))
            print(f"Saved metadata: {len(followers)} total followers, {new_followers_count} new in this batch")

            if not cursor:
                print("No more pages to fetch")
                break

            print("Waiting 60 seconds before next request...")
            time.sleep(60)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise RuntimeError(f"Failed to fetch followers: {e}") from e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise RuntimeError(f"Unexpected error occurred: {e}") from e
    return followers

if __name__ == "__main__":
    headers = cookies_headers.API_HEADERS
    user_id = "1260741614508691457"  # Amit
    base_filename = f"followers_{user_id}"

    print("Starting followers collection...")
    followers = get_followers(user_id, headers, max_usernames=224000, base_filename=base_filename)
    print(f"\nTotal followers retrieved: {len(followers)}")

    if followers:
        print("\nSample followers:")
        for i, follower in enumerate(followers[:5]):
            print(f"  {i+1}. @{follower['username']} - {follower['name']}")
        if len(followers) > 5:
            print(f"  ... and {len(followers) - 5} more")
