import requests

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_find_good_investors_x import headers, API_VARIABLES, API_FEATURES

variables = API_VARIABLES
variables['rawQuery'] = "from:sp3cul8r since:2025-02-19 until:2025-04-04"
variables['cursor'] = "dfd..."
features = API_FEATURES
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

cursor_entries = response_json["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"][0]["entries"]
for cursor_entry in cursor_entries:
    if "cursorType" in cursor_entry["content"] and cursor_entry["content"]["cursorType"] == "Top":
        cursor_value = cursor_entry["content"]["value"]
        print(cursor_value)
        break

tweet_entries = response_json["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"][0]["entries"]
for tweet_entry in tweet_entries:
    if tweet_entry["content"]["entryType"] == "TimelineTimelineItem":
        tweet_text = tweet_entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["full_text"]
        print(tweet_text)
