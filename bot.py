import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1491597296444637204/g8K4to4u2loQb_8JV5tQoARVb3VyxlzadYfF-rcLTNi82qSqFNG1YgWe47UHKByynNkI"

data = {
    "content": "🛒",
    "embeds": [
        {
            "title": "Rocket League Item Shop",
            "description": "Nowy sklep dostępny!\nhttps://rlshop.gg",
            "color": 10181046
        }
    ]
}

requests.post(WEBHOOK_URL, json=data)
