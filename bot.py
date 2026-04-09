import discord
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

URL = "https://rlshop.gg"


def get_items():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    # pobiera itemy ze strony (działa stabilnie)
    for item in soup.find_all("h3"):
        name = item.text.strip()

        # szukamy ceny obok
        parent = item.find_parent()
        price = parent.get_text()

        credits = "?"
        for word in price.split():
            if word.isdigit():
                credits = word

        if name:
            items.append({
                "name": name,
                "price": credits
            })

    return items


@tree.command(name="shop", description="Pokazuje sklep RL")
async def shop(interaction: discord.Interaction):
    items = get_items()

    embed = discord.Embed(
        title="🛒 Rocket League Shop",
        color=0x9b59b6
    )

    for item in items[:10]:
        embed.add_field(
            name=item["name"],
            value=f"💰 {item['price']} credits",
            inline=True
        )

    await interaction.response.send_message(embed=embed)


@tree.command(name="ping", description="Sprawdza czy bot działa")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")


@tree.command(name="help", description="Komendy bota")
async def help_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("/shop /ping /help")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
