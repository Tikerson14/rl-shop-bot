import discord
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import os
import asyncio
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 123456789012345678  # 🔥 TU WPISZ ID KANAŁU

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

URL = "https://rlshop.gg"


def get_items():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
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

    return items[:10]


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


@tree.command(name="shop", description="Pokazuje sklep RL")
async def shop(interaction: discord.Interaction):
    items = get_items()
    embed = create_embed(items)
    await interaction.response.send_message(embed=embed)


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
