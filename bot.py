import discord
from discord import app_commands
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1491559995287015565

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def get_shop():
    # 🔥 endpoint używany przez stronę (reverse)
    url = "https://rlshop.gg/api/shop"

    try:
        r = requests.get(url)

        if r.status_code != 200:
            return []

        data = r.json()

        items = []

        for item in data.get("featured", []):
            items.append({
                "name": item.get("name"),
                "price": item.get("price"),
                "image": item.get("image")
            })

        return items

    except:
        return []


def create_embed(items):
    embed = discord.Embed(
        title="🛒 Rocket League Shop",
        color=0x9b59b6
    )

    for item in items:
        embed.add_field(
            name=item["name"],
            value=f"💰 {item['price']} credits",
            inline=True
        )

    if items and items[0].get("image"):
        embed.set_image(url=items[0]["image"])

    return embed


@tree.command(name="shop", description="Prawdziwy sklep RL")
async def shop(interaction: discord.Interaction):
    items = get_shop()

    if not items:
        await interaction.response.send_message("❌ Nie udało się pobrać sklepu")
        return

    embed = create_embed(items)
    await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
