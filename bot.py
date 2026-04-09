import discord
from discord import app_commands
import asyncio
import os
from playwright.async_api import async_playwright

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1491559995287015565

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def get_items():
    items = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://rlshop.gg")
        await page.wait_for_timeout(3000)

        cards = await page.query_selector_all("h3")

        for card in cards[:10]:
            name = await card.inner_text()
            items.append(name)

        await browser.close()

    return items


@tree.command(name="shop", description="Pełny sklep RL")
async def shop(interaction: discord.Interaction):
    await interaction.response.defer()

    items = await get_items()

    embed = discord.Embed(
        title="🛒 Rocket League Shop",
        color=0x9b59b6
    )

    for item in items:
        embed.add_field(name=item, value="💰 sprawdź w sklepie", inline=True)

    await interaction.followup.send(embed=embed)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
