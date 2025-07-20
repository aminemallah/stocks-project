import requests
import json
import time
import os

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import cookies_headers

def load_saved_data(filename):
    """Load previously saved followers data and cursor"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('followers', []), data.get('cursor', None)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading saved data: {e}")
            return [], None
    return [], None

def save_data(filename, followers, cursor):
    """Save followers data and cursor to JSON file"""
    data = {
        'followers': followers,
        'cursor': cursor,
        'total_count': len(followers),
        'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(followers)} followers to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def get_followers(user_id, headers, max_usernames=100, save_filename='followers_data.json'):
    # Load previously saved data
    followers, saved_cursor = load_saved_data(save_filename)
    print(f"Loaded {len(followers)} previously saved followers")
    
    if saved_cursor:
        print(f"Resuming from cursor: {saved_cursor[:50]}...")
        cursor = saved_cursor
    else:
        cursor = None
    
    base_url = 'https://x.com/i/api/graphql/k8IHkYttROUDoDNevQ7Ehw/Followers'
    
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
            # Make API request
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Save raw response for debugging (optional)
            import sys
            import os
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
            from common import common_utils
            common_utils.save_json_file_to_disk("test.json", data)

            # Extract followers from response
            new_followers_count = 0
            next_cursor = None
            
            try:
                instructions = data['data']['user']['result']['timeline']['timeline']['instructions']
                for instruction in instructions:
                    if instruction['type'] == 'TimelineAddEntries':
                        for entry in instruction['entries']:
                            if entry['content']['entryType'] == 'TimelineTimelineItem':
                                try:
                                    user_data = entry['content']['itemContent']['user_results']['result']['core']
                                    username = user_data['screen_name']
                                    name = user_data['name']
                                    
                                    # Check if user already exists (avoid duplicates)
                                    if not any(follower['username'] == username for follower in followers):
                                        follower_info = {
                                            'username': username,
                                            'name': name
                                        }
                                        followers.append(follower_info)
                                        new_followers_count += 1
                                        print(f"Added follower {len(followers)}: @{username} ({name})")
                                    
                                    # Break if we reached max_usernames
                                    if len(followers) >= max_usernames:
                                        save_data(save_filename, followers, cursor)
                                        return followers
                                        
                                except (KeyError, TypeError) as e:
                                    print(f"Error parsing user data: {e}")
                                    continue

                            # Get next cursor
                            elif entry['content']['entryType'] == 'TimelineTimelineCursor' and entry['content']['cursorType'] == 'Bottom':
                                next_cursor = entry['content']["value"]
                                print(f"Found next cursor: {next_cursor[:50]}...")
            
            except (KeyError, TypeError) as e:
                print(f"Error parsing response: {e}")
                break

            # Update cursor for next iteration
            cursor = next_cursor
            
            # Save progress after each batch
            save_data(save_filename, followers, cursor)
            print(f"Saved progress: {len(followers)} total followers, {new_followers_count} new in this batch")

            # If no more cursor, break the loop
            if not cursor:
                print("No more pages to fetch")
                break

            # Rate limiting: sleep to avoid hitting API limits
            print("Waiting 60 seconds before next request...")
            time.sleep(60)

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            # Save current progress before breaking
            save_data(save_filename, followers, cursor)
            break

    # Final save
    save_data(save_filename, followers, None)  # Clear cursor when finished
    return followers

if __name__ == "__main__":
    headers = cookies_headers.API_HEADERS

    user_id = "1468103131737247748"  # Amit
    save_filename = f"followers_{user_id}.json"
    
    print("Starting followers collection...")
    followers = get_followers(user_id, headers, max_usernames=200000, save_filename=save_filename)
    print(f"\nTotal followers retrieved: {len(followers)}")
    
    # Print summary
    if followers:
        print("\nSample followers:")
        for i, follower in enumerate(followers[:5]):  # Show first 5
            print(f"  {i+1}. @{follower['username']} - {follower['name']}")
        if len(followers) > 5:
            print(f"  ... and {len(followers) - 5} more")