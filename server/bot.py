import discord
from discord.ext import commands
import os
import dotenv
import asyncio

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Commands:

@bot.command(name="list", description="to list all commands")
async def _list(ctx):
    command_list = [command.name for command in bot.commands]
    embed = discord.Embed(title="Available Commands", color=discord.Colour.blue())
    embed.description = "\n".join(command_list)
    await ctx.send(embed=embed)


# on ready code:

systemChannel = 1233588735115919381

@bot.event
async def on_ready():
    print("Bot is online and ready. System now Operational.")
    await asyncio.sleep(2) # Wait 2 seconds
    channel = bot.get_channel(systemChannel)
    if channel:
        await channel.send("Bot is online and ready. System now Operational.")

# bot run code:
bot.run(TOKEN)