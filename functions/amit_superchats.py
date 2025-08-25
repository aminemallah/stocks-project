from chat_downloader import ChatDownloader
from currency_converter import CurrencyConverter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.config_daily_fetch_amit_audience import keywords

blacklist = ["user1", "user2", "user3"]
links = [
"https://www.youtube.com/watch?v=Az9G8Ur0it8",
# "https://www.youtube.com/watch?v=AfPyBdd_Uz8",
"https://www.youtube.com/watch?v=0_icR59dJ2A",
"https://www.youtube.com/watch?v=ppT3DwSGzAs",
"https://www.youtube.com/watch?v=eKB5V8W51ts",
"https://www.youtube.com/watch?v=8dQXhffKEV0",
"https://www.youtube.com/watch?v=aHpbhik6PyM",
"https://www.youtube.com/watch?v=EfvbvIUIzTM",
"https://www.youtube.com/watch?v=_AUdmOeoycs",
"https://www.youtube.com/watch?v=2p04lyKXk3I&t=5475s",
"https://www.youtube.com/watch?v=ls7DyLSZMTg",
"https://www.youtube.com/watch?v=yWEIkkiOOTw",
"https://www.youtube.com/watch?v=fFP_4hcWzag&t=6664s",
"https://www.youtube.com/watch?v=aP3w6Gl0e-k&t=6263s",
"https://www.youtube.com/watch?v=zzd_6cc-A5E",
"https://www.youtube.com/watch?v=QrVHvm0w02c",
"https://www.youtube.com/watch?v=hPKsJnrWA8Y",
"https://www.youtube.com/watch?v=FOzXO88nvso",
"https://www.youtube.com/watch?v=hCe1-09Igag",
"https://www.youtube.com/watch?v=vh4yEnhnym4&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=4lHVQ2HIhBU",
"https://www.youtube.com/watch?v=M2u1-Io1gjo",
"https://www.youtube.com/watch?v=oo9mRRaviRc&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=95x2lspiM-U",
"https://www.youtube.com/watch?v=xx2HRwZsNhc",
"https://www.youtube.com/watch?v=2jsbkXpGx0c",
"https://www.youtube.com/watch?v=ttCGRiehspQ",
"https://www.youtube.com/watch?v=zewhSG-yZ9Y",
"https://www.youtube.com/watch?v=Nw5Kbvy1dzE",
"https://www.youtube.com/watch?v=rfOoYCKr4i4&t=4051s",
"https://www.youtube.com/watch?v=ubvGMdvxo_Q&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=Zk8ijJXXctQ",
"https://www.youtube.com/watch?v=XedDKI9kx5c&t=28s",
"https://www.youtube.com/watch?v=RyBWwtQYgiM",
"https://www.youtube.com/watch?v=bdhdKe7FjAU",
"https://www.youtube.com/watch?v=7IRYdlpmkDA&t=585s",
"https://www.youtube.com/watch?v=Erb0YvcRW70&t=1059s",
"https://www.youtube.com/watch?v=tAFdpT7jzhk",
"https://www.youtube.com/watch?v=VxXN9a4t_Kw",
"https://www.youtube.com/watch?v=cpL9oiOcnoI",
"https://www.youtube.com/watch?v=yF3zUQ_vFWc&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=d_zz54GgQgo&t=7273s",
"https://www.youtube.com/watch?v=-OPo1YiYbPE&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=Ed0KOsWPxJ0",
"https://www.youtube.com/watch?v=zUrUH4EiWzg&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=hM0wCFbGIuE",
"https://www.youtube.com/watch?v=NMD_8QQ6QEk",
"https://www.youtube.com/watch?v=9x3rNxfioKA",
"https://www.youtube.com/watch?v=b0anW1C6VdQ&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=klOWQ-qrExA",
"https://www.youtube.com/watch?v=ZNxsXdFZ148",
"https://www.youtube.com/watch?v=6tbXpQ97prY",
"https://www.youtube.com/watch?v=OtzTBCYw_00",
"https://www.youtube.com/watch?v=oTbpm377Za4",
"https://www.youtube.com/watch?v=TwxsBAuu5dw",
"https://www.youtube.com/watch?v=UORVYKi7Ur8&t=4980s",
"https://www.youtube.com/watch?v=2YulE0_wggg",
"https://www.youtube.com/watch?v=57RuDYCQ-WY",
"https://www.youtube.com/watch?v=UsxiGI0ybz4",
"https://www.youtube.com/watch?v=3fyNH_CeGtg",
"https://www.youtube.com/watch?v=hdbvtGnuwUE",
"https://www.youtube.com/watch?v=he1NsQdcd1U",
"https://www.youtube.com/watch?v=Hpk2TLhRQTY",
"https://www.youtube.com/watch?v=Ixxhe0S0z5k&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=yRvSSoASyo8&t=5271s",
"https://www.youtube.com/watch?v=xvAbmCvapoA",
"https://www.youtube.com/watch?v=E3C4hGcccqU",
"https://www.youtube.com/watch?v=W3_lYqt13Qo",
"https://www.youtube.com/watch?v=VphCZs1ThBY",
"https://www.youtube.com/watch?v=S9wEH4dOGf0",
"https://www.youtube.com/watch?v=M9thNJWLxFU&t=361s&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=SEUjJ9XT43E",
"https://www.youtube.com/watch?v=CDYpvMOuTkA&t=8292s",
"https://www.youtube.com/watch?v=cDgu9zE_360",
"https://www.youtube.com/watch?v=eQqlKFMCRvk",
"https://www.youtube.com/watch?v=EP3EaTnoJ6g",
"https://www.youtube.com/watch?v=IyMBPtjeP5M",
"https://www.youtube.com/watch?v=rRtltplhCW4&t=270s",
"https://www.youtube.com/watch?v=cLyEfCEfVRI",
"https://www.youtube.com/watch?v=F-zIZ6yzG00&t=3128s",
"https://www.youtube.com/watch?v=qKi1eKK1oGQ",
"https://www.youtube.com/watch?v=JzUf6hH-Drg",
"https://www.youtube.com/watch?v=Iq1XQcpL7eg&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=W946BKMEhiw&t=1016s",
"https://www.youtube.com/watch?v=7WSAcLar1Ek&t=9932s",
"https://www.youtube.com/watch?v=s67ui9Jv0Hs",
"https://www.youtube.com/watch?v=E7ABmDTxLIo&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=KSBQx8te25s",
"https://www.youtube.com/watch?v=4suiUT1VT0U",
"https://www.youtube.com/watch?v=H4nizyAPcc8",
"https://www.youtube.com/watch?v=od9cLcekrmA",
"https://www.youtube.com/watch?v=ZjxgMRu-loE&t=14s",
"https://www.youtube.com/watch?v=C2HHXTspBWs",
"https://www.youtube.com/watch?v=E9YRrjvbPII&t=1s",
"https://www.youtube.com/watch?v=C0190ftJusw",
"https://www.youtube.com/watch?v=GJMULPRD68Q",
"https://www.youtube.com/watch?v=zMm738PQPeU&pp=0gcJCa0JAYcqIYzv",
"https://www.youtube.com/watch?v=9iMv9mWp-zg",
"https://www.youtube.com/watch?v=m0ba17at9l8",
"https://www.youtube.com/watch?v=QKUMGYNL_W0",
"https://www.youtube.com/watch?v=WhLeQoLY4vk",
"https://www.youtube.com/watch?v=H2KOzymkwJ4",
"https://www.youtube.com/watch?v=DEHBYUaVTS0",
"https://www.youtube.com/watch?v=0_icR59dJ2A",
"https://www.youtube.com/watch?v=eKB5V8W51ts",]

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
