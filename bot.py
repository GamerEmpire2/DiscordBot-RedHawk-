import discord
from discord.ext import commands
import os
import dotenv

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

bot.run(TOKEN)