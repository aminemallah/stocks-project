import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_daily_fetch_amit_audience import headers
from common import common_utils
from functions import amit_chats

PROCESSED_LINKS_FILE = "data/processed_amit_yt_links.jsonl"

def load_processed_links():
    processed_links = set()
    if os.path.exists(PROCESSED_LINKS_FILE):
        with open(PROCESSED_LINKS_FILE, 'r') as f:
            for line in f:
                processed_links.add(line.strip())
    return processed_links

def save_processed_link(link):
    with open(PROCESSED_LINKS_FILE, 'a') as f:
        f.write(link + '\n')

processed_links = load_processed_links()

response = requests.get('https://www.youtube.com/@amitinvesting/streams', params={'themeRefresh': '1'}, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

script_tags = soup.find_all('script')

yt_initial_data = {}

for script in script_tags:
    if script.string and 'var ytInitialData =' in script.string:
        script_content = script.string
        match = re.search(r'var ytInitialData = ({.*?});', script_content, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                yt_initial_data = json.loads(json_str)
                break
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                exit()

video_count = 0
for yt_obj in yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][3]['tabRenderer']['content']['richGridRenderer']['contents'][:4]:
    if video_count >= 2:
        break
    ytvid_id = yt_obj['richItemRenderer']['content']['videoRenderer']['videoId']
    ytvid_url = f"https://www.youtube.com/watch?v={ytvid_id}"
    if ytvid_url not in processed_links:
        print(ytvid_id)
        chats = amit_chats.run(ytvid_url)
        concatenated_chats = "\n".join(chats)
        # Handle messages in batches of 4000 characters
        max_length = 4000
        for i in range(0, len(concatenated_chats), max_length):
            batch = concatenated_chats[i:i + max_length]
            common_utils.notify_message_aleph(batch)
        save_processed_link(ytvid_url)
        video_count += 1