from chat_downloader import ChatDownloader
from currency_converter import CurrencyConverter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_daily_fetch_amit_audience import keywords

blacklist = ["user1", "user2", "user3"]
links = [
"https://www.youtube.com/watch?v=WlEzNX-XPQk",
"https://www.youtube.com/watch?v=s1If30m3jYk&pp=2Ab_Lw%3D%3D",
"https://www.youtube.com/watch?v=mSf1VU-er7o&pp=2AbpSA%3D%3D",
"https://www.youtube.com/watch?v=ckcsn7zL7xg&pp=2Ab4TQ%3D%3D",
"https://www.youtube.com/watch?v=jSnF0mHirj8&pp=0gcJCbIJAYcqIYzv",
"https://www.youtube.com/watch?v=81g2t4uYafw&pp=2Aa3Sg%3D%3D",
"https://www.youtube.com/watch?v=goAkGJ6oc_A",
"https://www.youtube.com/watch?v=UhIONspSaYU&pp=2AbYCQ%3D%3D",
"https://www.youtube.com/watch?v=jGVSlabUFKY&pp=2AYV",
"https://www.youtube.com/watch?v=1KHqS4EcNDI",
"https://www.youtube.com/watch?v=9eYo_m_gAjk&pp=2AbOGdIHCQmyCQGHKiGM7w%3D%3D",
"https://www.youtube.com/watch?v=H2KOzymkwJ4&pp=0gcJCbIJAYcqIYzv",
"https://www.youtube.com/watch?v=DEHBYUaVTS0",
"https://www.youtube.com/watch?v=0_icR59dJ2A&pp=0gcJCbIJAYcqIYzv",
"https://www.youtube.com/watch?v=eKB5V8W51ts",
"https://www.youtube.com/watch?v=2p04lyKXk3I&pp=2AbpKg%3D%3D",
"https://www.youtube.com/watch?v=fFP_4hcWzag&pp=2AaKNA%3D%3D",
"https://www.youtube.com/watch?v=QrVHvm0w02c",
"https://www.youtube.com/watch?v=rfOoYCKr4i4&pp=2AbTHw%3D%3D",
"https://www.youtube.com/watch?v=Zk8ijJXXctQ",
"https://www.youtube.com/watch?v=hM0wCFbGIuE",
"https://www.youtube.com/watch?v=b0anW1C6VdQ&pp=0gcJCbIJAYcqIYzv",
"https://www.youtube.com/watch?v=UORVYKi7Ur8&pp=2Ab-Jg%3D%3D",
"https://www.youtube.com/watch?v=UsxiGI0ybz4&pp=2AadKg%3D%3D",
"https://www.youtube.com/watch?v=hdbvtGnuwUE&pp=0gcJCbIJAYcqIYzv",
"https://www.youtube.com/watch?v=yRvSSoASyo8&pp=2AacJA%3D%3D",
"https://www.youtube.com/watch?v=E3C4hGcccqU",
"https://www.youtube.com/watch?v=CDYpvMOuTkA&pp=2AbkQA%3D%3D",
"https://www.youtube.com/watch?v=cLyEfCEfVRI",
]

c = CurrencyConverter()
qualified_users = set()
user_donations = {}
total_donations = 0
all_messages = []   # store all messages for second pass

log_file = "superchat_log.txt"

for url in links:
    print(f"\nProcessing video: {url}")
    try:
        chat = ChatDownloader().get_chat(url, message_groups=['messages', 'superchat'])

        # -------- PASS 1: Find qualified users --------
        for message in chat:
            author = message.get('author', {}).get('name', 'Unknown')
            if author.lower() in [name.lower() for name in blacklist]:
                continue

            # Save all messages for pass 2
            all_messages.append(message)

            # Handle Superchat
            money = message.get('money', {})
            amount = money.get('amount', 0)
            currency = money.get('currency', 'USD')

            if currency != "USD" and currency is not None:
                try:
                    amount = c.convert(amount, currency, 'USD')
                except Exception as e:
                    print(f"Currency conversion error for {author}: {e}")
                    continue

            if amount > 49:
                qualified_users.add(author)
                if author not in user_donations:
                    user_donations[author] = []
                user_donations[author].append(amount)
                total_donations += amount

    except Exception as e:
        print(f"Error processing {url}: {e}")

# -------- PASS 2: Collect messages for qualified users --------
user_messages = {}
for message in all_messages:
    author = message.get('author', {}).get('name', 'Unknown')
    if author in qualified_users:
        text = message.get('message', '')
        timestamp = message.get('time_in_seconds', 0)
        if author not in user_messages:
            user_messages[author] = []
        user_messages[author].append(f"{timestamp:.2f} | {text}")

# -------- SAVE RESULTS --------
with open(log_file, "w", encoding="utf-8") as f:
    for user in sorted(qualified_users):
        donations = [f"${amt:.2f}" for amt in user_donations.get(user, [])]
        total_user_amount = sum(user_donations.get(user, []))
        f.write(f"User: {user}\n")
        f.write(f"Total Donations: ${total_user_amount:.2f}\n")
        f.write(f"Superchats: {', '.join(donations)}\n")
        f.write("Messages:\n")
        for msg in user_messages.get(user, []):
            f.write(f"  {msg}\n")
        f.write("\n" + "="*50 + "\n\n")

print("\nUnique users with Superchats > $49 USD equivalent across all videos:")
for user in sorted(qualified_users):
    total_user_amount = sum(user_donations[user])
    print(f"{user}: ${total_user_amount:.2f} USD")

print(f"\nTotal donations across all users: ${total_donations:.2f} USD")
print(f"Log file saved to: {os.path.abspath(log_file)}")
