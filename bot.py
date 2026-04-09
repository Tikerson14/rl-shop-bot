import requests
from bs4 import BeautifulSoup
import hashlib
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1491597296444637204/g8K4to4u2loQb_8JV5tQoARVb3VyxlzadYfF-rcLTNi82qSqFNG1YgWe47UHKByynNkI"
URL = "https://rlshop.gg"
FILE = "last_shop.txt"

def get_items():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    # znajdź itemy (może się zmienić!)
    for item in soup.find_all("h3"):
        text = item.text.strip()
        if text:
            items.append(text)

    return items[:6]  # max 6 itemów

def get_hash(items):
    return hashlib.md5("".join(items).encode()).hexdigest()

def load_last():
    if os.path.exists(FILE):
        return open(FILE).read()
    return None

def save_last(hash_value):
    with open(FILE, "w") as f:
        f.write(hash_value)

def send_embed(items):
    description = "\n".join([f"• {item}" for item in items])

    data = {
        "content": "🛒",
        "embeds": [
            {
                "author": {
                    "name": "Rocket League Shop",
                    "icon_url": "https://rl.insider.gg/images/logos/rlg.png"
                },
                "title": "🔥 Daily Item Shop",
                "description": description,
                "color": 10181046,
                "footer": {
                    "text": "Auto Tracker PRO"
                }
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=data)

def commit_file():
    os.system("git config --global user.name 'bot'")
    os.system("git config --global user.email 'bot@github.com'")
    os.system("git add last_shop.txt")
    os.system("git commit -m 'update shop'")
    os.system("git push")

def main():
    items = get_items()
    current_hash = get_hash(items)
    last_hash = load_last()

    if current_hash != last_hash:
        print("Nowy sklep!")
        send_embed(items)
        save_last(current_hash)
        commit_file()
    else:
        print("Brak zmian")

if __name__ == "__main__":
    main()
