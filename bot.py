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
    for item in soup.find_all("h3"):
        text = item.text.strip()
        if text:
            items.append(text)

    return items[:5]

@tree.command(name="shop", description="Pokazuje aktualny sklep")
async def shop(interaction: discord.Interaction):
    items = get_items()
    text = "\n".join([f"• {i}" for i in items])

    embed = discord.Embed(
        title="🛒 Rocket League Shop",
        description=text,
        color=0x9b59b6
    )

    await interaction.response.send_message(embed=embed)

@tree.command(name="ping", description="Sprawdza czy bot działa")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")

@tree.command(name="help", description="Komendy bota")
async def help_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("/shop\n/ping\n/help")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Zalogowano jako {client.user}")

client.run(TOKEN)
