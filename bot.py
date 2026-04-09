import discord
from discord import app_commands
import asyncio
import os
from playwright.async_api import async_playwright

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# 🔥 POBIERANIE ITEMÓW (SZYBSZE + STABILNE)
async def get_items():
    items = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://rlshop.gg")

        # 🔥 szybkie czekanie zamiast sleep
        await page.wait_for_selector("h3", timeout=3000)

        cards = await page.query_selector_all("h3")

        for card in cards[:10]:
            name = await card.inner_text()
            items.append(name)

        await browser.close()

    return items


# 🔥 KOMENDA /shop (NAPRAWIONA)
@tree.command(name="shop", description="Pełny sklep Rocket League")
async def shop(interaction: discord.Interaction):

    try:
        # 🔥 NATYCHMIASTOWA ODPOWIEDŹ (usuwa error 10062)
        await interaction.response.defer(thinking=True)

        items = await get_items()

        if not items:
            await interaction.followup.send("❌ Nie udało się pobrać sklepu")
            return

        embed = discord.Embed(
            title="🛒 Rocket League Shop",
            description="📅 Daily Shop",
            color=0x9b59b6
        )

        for item in items:
            embed.add_field(
                name=f"🔥 {item}",
                value="💰 sprawdź w sklepie",
                inline=True
            )

        # 🔥 zabezpieczenie przed expired interaction
        if interaction.is_expired():
            return

        await interaction.followup.send(embed=embed)

    except Exception as e:
        try:
            await interaction.followup.send(f"❌ Błąd: {e}")
        except:
            print("Interaction expired")


# 🔥 TEST
@tree.command(name="ping", description="Sprawdza bota")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")


# 🔥 START
@client.event
async def on_ready():
    await tree.sync()
    print(f"Zalogowano jako {client.user}")


client.run(TOKEN)
