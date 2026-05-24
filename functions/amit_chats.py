import sys
import os
import json
import threading
import time
from datetime import datetime
from chat_downloader import ChatDownloader
from chat_downloader.errors import NoChatReplay, VideoUnplayable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_daily_fetch_amit_audience import keywords  # assuming this exists

class TimeoutException(Exception):
    pass

def run(url, timeout_seconds=200):  # 10 minutes = 600 seconds
    os.makedirs("data", exist_ok=True)

    output_filename = "data/youtube_chat.txt"
    raw_output_filename = "data/youtube_chat_raw.json"
    raw_messages = []

    try:
        chat = ChatDownloader().get_chat(url, message_groups=['messages'])
    except NoChatReplay:
        print(f"Video does not have a chat replay: {url}")
        return []
    except VideoUnplayable as e:
        print(f"Video is not accessible (members-only or restricted): {url}")
        return []

    # Append mode for the text log
    need_header = (not os.path.exists(output_filename)) or (os.path.getsize(output_filename) == 0)
    with open(output_filename, 'a', encoding='utf-8') as f, open(raw_output_filename, 'w', encoding='utf-8') as raw_f:
        if need_header:
            f.write(f"YouTube Chat Log - cumulative\n")
            f.write(f"First capture: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")

        f.write(f"--- New capture for URL: {url} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        
        start_time = time.time()
        message_count = 0
        
        for message in chat:
            # Check if we've exceeded the timeout
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout_seconds:
                print(f"\nTimeout reached ({timeout_seconds}s) while waiting for messages. Video may not have started yet: {url}")
                return None  # Return None to indicate timeout (don't add to processed list)
            
            author = message.get('author', {}).get('name', 'Unknown')
            text = message.get('message', '')
            money = message.get('money')
            message_count += 1

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

    print(f"\nAppended {message_count} chat messages to: {output_filename}")
    print(f"Raw message subset saved to (overwritten each run): {raw_output_filename}")
    return raw_messages

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    run(url)




