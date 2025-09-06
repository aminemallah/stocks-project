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

yt_channels = [
    "https://www.youtube.com/@amitinvesting/streams",
    "https://www.youtube.com/@RealMattMoney/streams",
    "https://www.youtube.com/@Funofinvesting/streams",
    "https://www.youtube.com/@futurenvesting/streams"
]

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

def process_channel(channel_url):
    response = requests.get(channel_url, params={'themeRefresh': '1'}, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the page for {channel_url}. Status code: {response.status_code}")
        return

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
                    print(f"Error parsing JSON for {channel_url}: {e}")
                    return

    video_count = 0
    try:
        videos = yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][3]['tabRenderer']['content']['richGridRenderer']['contents'][:4]
    except KeyError:
        print(f"Could not parse videos for {channel_url}")
        return

    for yt_obj in videos:
        if video_count >= 2:
            break
        if 'richItemRenderer' in yt_obj and 'videoRenderer' in yt_obj['richItemRenderer']['content']:
            ytvid_id = yt_obj['richItemRenderer']['content']['videoRenderer']['videoId']
            ytvid_url = f"https://www.youtube.com/watch?v={ytvid_id}"
            if ytvid_url not in processed_links:
                print(f"Processing video: {ytvid_id} from {channel_url}")
                chats = amit_chats.run(ytvid_url)
                concatenated_chats = "\n".join(chats)
                max_length = 3500
                for i in range(0, len(concatenated_chats), max_length):
                    batch = concatenated_chats[i:i + max_length]
                    common_utils.notify_message_aleph(batch)
                save_processed_link(ytvid_url)
                processed_links.add(ytvid_url)
                video_count += 1

if __name__ == "__main__":
    for channel in yt_channels:
        process_channel(channel)
