from chat_downloader import ChatDownloader
from currency_converter import CurrencyConverter

blacklist = ["user1", "user2", "user3"]
links = [
    "https://www.youtube.com/watch?v=RpFGNkhVJUc",
    "https://www.youtube.com/watch?v=1s-ov1jHgPQ&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=fKk-p_DI8so",
    "https://www.youtube.com/watch?v=aMKdkefZQiQ",
    "https://www.youtube.com/watch?v=HpeAKKUySsY",
    "https://www.youtube.com/watch?v=mglvN2mxBqk",
    "https://www.youtube.com/watch?v=rU8aj00TVkE",
    "https://www.youtube.com/watch?v=Y8XQhcEvU6E",
    "https://www.youtube.com/watch?v=3cNxGUftbg4",
    "https://www.youtube.com/watch?v=oEhUr1VNFHg",
    "https://www.youtube.com/watch?v=QQ1_VxjqOG8",
    "https://www.youtube.com/watch?v=-_89G9DEVBk",
    "https://www.youtube.com/watch?v=rQi5F9stfWo",
    "https://www.youtube.com/watch?v=dBD08qhVToI",
    "https://www.youtube.com/watch?v=QUE5oCBTujQ",
    "https://www.youtube.com/watch?v=i2FgDjfiijc",
    "https://www.youtube.com/watch?v=_ybuKRuiQAM",
    "https://www.youtube.com/watch?v=3HAhxrBQQKo",
    "https://www.youtube.com/watch?v=TaW3liTZgDw",
    "https://www.youtube.com/watch?v=taqYtYXChCg",
    "https://www.youtube.com/watch?v=eiTzO9B6nqs",
    "https://www.youtube.com/watch?v=ihKtkPJaeKg",
    "https://www.youtube.com/watch?v=auM0rfZTQD0",
    "https://www.youtube.com/watch?v=Cn518augEZY&t=7914s",
    "https://www.youtube.com/watch?v=Lok50jinhMs&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=gfq2WPG7bV4&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=81ay9XdlAW8",
    "https://www.youtube.com/watch?v=6HUX6Q1zkgM&t=1441s",
    "https://www.youtube.com/watch?v=x4ISEOulfdU",
    "https://www.youtube.com/watch?v=TRgjaq0QIxY",
    "https://www.youtube.com/watch?v=N4YijPBJAcU",
    "https://www.youtube.com/watch?v=27gTKoLmHx8&t=6143s",
    "https://www.youtube.com/watch?v=Y8PSrjdsUco",
    "https://www.youtube.com/watch?v=tneMeoJY6Vo&t=1166s",
    "https://www.youtube.com/watch?v=zRXv9fNAXLI",
    "https://www.youtube.com/watch?v=SUkua8sJhNg",
    "https://www.youtube.com/watch?v=BtXpg9qDqRc",
    "https://www.youtube.com/watch?v=jnebtnYvXw4&t=8070s",
    "https://www.youtube.com/watch?v=tTuquG4OGrc&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=i6dfQktioAs",
    "https://www.youtube.com/watch?v=UzxHklKVe9o",
    "https://www.youtube.com/watch?v=03MBnCI6VJA",
    "https://www.youtube.com/watch?v=XhShE1PsNW0",
    "https://www.youtube.com/watch?v=Qd0jX5rH4-A",
    "https://www.youtube.com/watch?v=VwyhGKa_700",
    "https://www.youtube.com/watch?v=BQWivaWmwX0&t=6712s",
    "https://www.youtube.com/watch?v=-1wGfmiq7Rw&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=avu6hSyHRPE",
    "https://www.youtube.com/watch?v=GuJKV0guJno",
    "https://www.youtube.com/watch?v=_FbsWIzbAJE",
    "https://www.youtube.com/watch?v=s7QpkgwTp14",
    "https://www.youtube.com/watch?v=k9W4-dOGZDk",
    "https://www.youtube.com/watch?v=1ZaFAXemad4",
    "https://www.youtube.com/watch?v=ke6-bRmvCzA",
    "https://www.youtube.com/watch?v=uHmWUNIOU78",
    "https://www.youtube.com/watch?v=P4EYjDjVh9Q",
    "https://www.youtube.com/watch?v=3E7eL0Cp20U",
    "https://www.youtube.com/watch?v=evgG3_H7tyw",
    "https://www.youtube.com/watch?v=HFgoDrs_G1U",
    "https://www.youtube.com/watch?v=WXhE7Oi_fJU",
    "https://www.youtube.com/watch?v=f3Xd6LYZOso&t=1s",
    "https://www.youtube.com/watch?v=H5lnpFZSVF0",
    "https://www.youtube.com/watch?v=CmXJqzi9x1Y",
    "https://www.youtube.com/watch?v=uUytkRwQwrg&t=8106s&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=gCysa53eMdw",
    "https://www.youtube.com/watch?v=EODsAHVMN9o",
    "https://www.youtube.com/watch?v=0D_t1_epRgw&t=10914s",
    "https://www.youtube.com/watch?v=GiiTAFoaOYk",
    "https://www.youtube.com/watch?v=5lh6-obXLT8",
    "https://www.youtube.com/watch?v=09reXWqFfPA&pp=0gcJCccJAYcqIYzv",
    "https://www.youtube.com/watch?v=7LckTZM_x7I",
    "https://www.youtube.com/watch?v=IgYvBeC9rAU",
    "https://www.youtube.com/watch?v=LA4rSTwe0Ts",
    "https://www.youtube.com/watch?v=CgDkdSzGp_w",
    "https://www.youtube.com/watch?v=p8QPc5jZoO0",
    "https://www.youtube.com/watch?v=rBvu6BcA83o",
    "https://www.youtube.com/watch?v=CD-3dfOPFmI",
    "https://www.youtube.com/watch?v=uP0GNTnPsTc",
    "https://www.youtube.com/watch?v=Bq63G6ZMxvU",
    "https://www.youtube.com/watch?v=4fXKoptZQUs",
    "https://www.youtube.com/watch?v=0a1zViFyFNI",
    "https://www.youtube.com/watch?v=9uVKBsx0tpc",
    "https://www.youtube.com/watch?v=mq6OPE23mLA",
    "https://www.youtube.com/watch?v=g1AiOCiHxuE",
    "https://www.youtube.com/watch?v=KWZV2qt6Ui8&t=20s",
    "https://www.youtube.com/watch?v=RJ0HUQRE0Ts&t=2s",
    "https://www.youtube.com/watch?v=T4YNmMdjq6E"
]

c = CurrencyConverter()
unique_users = set()
user_donations = {}
total_donations = 0

for url in links:
    print(f"\nProcessing video: {url}")
    try:
        chat = ChatDownloader().get_chat(url, message_groups=['superchat'])
        for message in chat:
            author = message.get('author', {}).get('name', 'Unknown')
            if author.lower() in [name.lower() for name in blacklist]:
                continue
            
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
                unique_users.add(author)
                if author not in user_donations:
                    user_donations[author] = []
                user_donations[author].append(amount)
                total_donations += amount
                timestamp = message.get('time_in_seconds', 0)
                text = message.get('message', '')
                print(f"{timestamp:.2f} | {author}: {currency}${amount:.2f} (~${amount:.2f} USD) - {text}")
                
    except Exception as e:
        print(f"Error processing {url}: {e}")

print("\nUnique users with Superchats > $50 USD equivalent across all videos:")
for user in sorted(unique_users):
    donations = [f"${amt:.2f}" for amt in user_donations[user]]
    total_user_amount = sum(user_donations[user])
    print(f"{user}: {', '.join(donations)} USD (Total: ${total_user_amount:.2f} USD)")

print(f"\nTotal donations across all users: ${total_donations:.2f} USD")