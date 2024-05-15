import discord
from discord.ext import commands
import os
import logging
import logger
import asyncio

systemChannel = 1233588735115919381
LOG_CHANNEL_ID = 1240158663004389467

TOKEN2 = os.getenv("TOKEN2")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_message(message):
    # Check if the message is from a bot or from the logging channel itself
    if message.author.bot or message.channel.id == LOG_CHANNEL_ID:
        return

    # Create an embed for the log message
    embed = discord.Embed(
        title="Message Log",
        description=message.content,
        color=discord.Color.blue()
    )
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    embed.set_footer(text=f"Sent in #{message.channel.name}")

    # Fetch the logging channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    # Send the embed to the logging channel
    await log_channel.send(embed=embed)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    await asyncio.sleep(2)
    channel = bot.get_channel(systemChannel)
    if channel:
        await channel.send("logger bot is online")

bot.run(TOKEN2)