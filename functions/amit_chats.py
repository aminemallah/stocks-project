import sys
import os
import json
from datetime import datetime
from chat_downloader import ChatDownloader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_daily_fetch_amit_audience import keywords  # assuming this exists

def run(url):
    os.makedirs("data", exist_ok=True)

    output_filename = "data/youtube_chat.txt"
    raw_output_filename = "data/youtube_chat_raw.json"
    raw_messages = []

    chat = ChatDownloader().get_chat(url, message_groups=['messages'])

    # Append mode for the text log
    need_header = (not os.path.exists(output_filename)) or (os.path.getsize(output_filename) == 0)
    with open(output_filename, 'a', encoding='utf-8') as f, open(raw_output_filename, 'w', encoding='utf-8') as raw_f:
        if need_header:
            f.write(f"YouTube Chat Log - cumulative\n")
            f.write(f"First capture: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")

        f.write(f"--- New capture for URL: {url} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        for message in chat:
            author = message.get('author', {}).get('name', 'Unknown')
            text = message.get('message', '')
            money = message.get('money')

            f.write(f"{message.get('message_type', '')} | {author}: {text}\n")

            try:
                if any(keyword.lower() in author.lower() for keyword in keywords):
                    chat.print_formatted(message)
                    if money is not None:
                        raw_messages.append(f"{author} - {money['text']}: {text}")
                    else:
                        raw_messages.append(f"{author}: {text}")
            except NameError:
                pass

        f.write("\n")  # blank line between runs
        json.dump(raw_messages, raw_f, ensure_ascii=False, indent=2)

    print(f"\nAppended chat messages to: {output_filename}")
    print(f"Raw message subset saved to (overwritten each run): {raw_output_filename}")
    return raw_messages

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    run(url)




