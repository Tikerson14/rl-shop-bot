import discord
from discord import app_commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def get_items():
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


@tree.command(name="shop", description="Pokazuje sklep RL")
async def shop(interaction: discord.Interaction):
    items = get_items()

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

    await interaction.response.send_message(embed=embed)


@tree.command(name="ping", description="Sprawdza czy bot działa")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
