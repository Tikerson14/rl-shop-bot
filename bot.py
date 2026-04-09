import discord
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import os
import asyncio
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")

# 🔥 WSTAW ID KANAŁU (prawy klik → kopiuj ID)
CHANNEL_ID = 1491559995287015565

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

URL = "https://rlshop.gg"


# 🔥 fallback (zawsze działa jeśli scraping padnie)
def fallback_items():
    return [
        {"name": "Takumi RX-T", "price": "700"},
        {"name": "Solar Flare", "price": "2200"},
        {"name": "Almagest", "price": "900"},
        {"name": "Krew Made", "price": "500"},
        {"name": "SLK", "price": "400"},
        {"name": "Electroshock", "price": "2200"},
        {"name": "Astro-CSX", "price": "900"},
        {"name": "Tsunami Beam", "price": "700"}
    ]


def get_items():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9"
        }

        r = requests.get(URL, headers=headers, timeout=10)

        if r.status_code != 200:
            print("❌ Status != 200")
            return fallback_items()

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

            if name and len(name) < 40:
                items.append({
                    "name": name,
                    "price": price
                })

        if not items:
            print("❌ Brak itemów → fallback")
            return fallback_items()

        print("✅ ITEMY:", items[:5])

        return items[:10]

    except Exception as e:
        print("❌ ERROR:", e)
        return fallback_items()


def create_embed(items):
    embed = discord.Embed(
        title="🛒 Rocket League Shop",
        description="📅 Daily Shop\n⏰ Reset: 21:00",
        color=0x9b59b6
    )

    for item in items:
        embed.add_field(
            name=item["name"],
            value=f"💰 {item['price']} credits",
            inline=True
        )

    return embed


# 🔥 KOMENDA
@tree.command(name="shop", description="Pokazuje sklep RL")
async def shop(interaction: discord.Interaction):
    items = get_items()
    embed = create_embed(items)
    await interaction.response.send_message(embed=embed)


# 🔥 AUTO SHOP
async def auto_shop():
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.now()

        if now.hour == 21 and now.minute == 0:
            channel = client.get_channel(CHANNEL_ID)

            if channel:
                items = get_items()
                embed = create_embed(items)
                await channel.send(embed=embed)

            await asyncio.sleep(60)

        await asyncio.sleep(10)


@client.event
async def on_ready():
    await tree.sync()
    client.loop.create_task(auto_shop())
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
