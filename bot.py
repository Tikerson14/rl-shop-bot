import requests
from bs4 import BeautifulSoup
import hashlib
import os

WEBHOOK_URL = "TU_WKLEJ_WEBHOOK"
URL = "https://rlshop.gg"
FILE = "last_shop.txt"

def get_shop():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.title.string.strip()

def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def load_last():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return f.read()
    return None

def save_last(hash_value):
    with open(FILE, "w") as f:
        f.write(hash_value)

def send_embed():
    data = {
        "content": "🛒",
        "embeds": [
            {
                "author": {
                    "name": "Rocket League Shop",
                    "icon_url": "https://rl.insider.gg/images/logos/rlg.png"
                },
                "title": "🔥 Nowy Item Shop!",
                "description": "Kliknij żeby zobaczyć:\nhttps://rlshop.gg",
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
    shop = get_shop()
    current_hash = get_hash(shop)
    last_hash = load_last()

    if current_hash != last_hash:
        print("Nowy sklep!")
        send_embed()
        save_last(current_hash)
        commit_file()
    else:
        print("Brak zmian")

if __name__ == "__main__":
    main()
