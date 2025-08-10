import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_daily_fetch_amit_audience import keywords

import json
from datetime import datetime
from chat_downloader import ChatDownloader

def run(url):
    output_filename = f"data/youtube_chat.txt"
    raw_output_filename = f"data/youtube_chat_raw.json"
    raw_messages = []

    chat = ChatDownloader().get_chat(url, message_groups=['messages', 'superchat'])

    with open(output_filename, 'w', encoding='utf-8') as f, open(raw_output_filename, 'w', encoding='utf-8') as raw_f:
        f.write(f"YouTube Chat Log - {url}\n")
        f.write(f"Captured on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        for message in chat:
            author = message.get('author', {}).get('name', 'Unknown')
            text = message.get('message', '')
            money = message.get('money', None)

            f.write(f"{message.get('message_type', '')} | {author}: {text}\n")

            try:
                if any(author == keyword for keyword in keywords) or money is not None:
                    chat.print_formatted(message)
                    if money is not None:
                        raw_messages.append(f"{author} - {money['text']}: {text}")
                    else:
                        raw_messages.append(f"{author}: {text}")
            except NameError:
                pass
        json.dump(raw_messages, raw_f, ensure_ascii=False, indent=2)
    print(f"\nAll chat messages saved to: {output_filename}")
    print(f"Raw message objects saved to: {raw_output_filename}")
    return raw_messages

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    run(url)

