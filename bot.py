import discord
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import os
import asyncio
from datetime import datetime
import hashlib

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1491559995287015565  # 🔥 WSTAW ID

URL = "https://rlshop.gg"
LAST_HASH_FILE = "last_shop.txt"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def fallback_items():
    return [
        {"name": "Takumi RX-T", "price": "700"},
        {"name": "Solar Flare", "price": "2200"},
        {"name": "Almagest", "price": "900"},
        {"name": "Krew Made", "price": "500"},
        {"name": "SLK", "price": "400"}
    ]


def get_items():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        items = []

        for item in soup.find_all("h3"):
            name = item.text.strip()
            parent = item.find_parent()

            text = parent.get_text()
            price = "?"

            for word in text.split():
                if word.isdigit():
                    price = word

            if name:
                items.append({
                    "name": name,
                    "price": price
                })

        if not items:
            return fallback_items()

        return items[:10]

    except:
        return fallback_items()


def generate_hash(items):
    text = "".join([i["name"] + i["price"] for i in items])
    return hashlib.md5(text.encode()).hexdigest()


def load_last_hash():
    if os.path.exists(LAST_HASH_FILE):
        with open(LAST_HASH_FILE, "r") as f:
            return f.read()
    return None


def save_hash(h):
    with open(LAST_HASH_FILE, "w") as f:
        f.write(h)


def create_embed(items):
    embed = discord.Embed(
        title="🛒 Rocket League Shop",
        description="📅 Daily Shop\n⏰ Reset: 21:00",
        color=0x9b59b6
    )

    for item in items:
        embed.add_field(
            name=f"🔥 {item['name']}",
            value=f"💰 {item['price']} credits",
            inline=True
        )

    # 🔥 losowy obrazek (lepszy wygląd)
    embed.set_image(url="https://rocket-league.com/content/media/items/avatar/2200.png")

    return embed


@tree.command(name="shop", description="Pokazuje sklep RL")
async def shop(interaction: discord.Interaction):
    items = get_items()
    embed = create_embed(items)
    await interaction.response.send_message(embed=embed)


# 🔔 AUTO SHOP (bez spamu)
async def auto_shop():
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.now()

        if now.hour == 21 and now.minute == 0:
            items = get_items()
            new_hash = generate_hash(items)
            old_hash = load_last_hash()

            if new_hash != old_hash:
                channel = client.get_channel(CHANNEL_ID)

                if channel:
                    embed = create_embed(items)
                    await channel.send("🔥 **NOWY SKLEP!**", embed=embed)

                save_hash(new_hash)

            await asyncio.sleep(60)

        await asyncio.sleep(10)


@tree.command(name="ping", description="Sprawdza bota")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")


@client.event
async def on_ready():
    await tree.sync()
    client.loop.create_task(auto_shop())
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
