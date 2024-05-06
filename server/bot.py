import discord
from discord.ext import commands
import os
import dotenv
import asyncio
import subprocess
import requests

# this will be your GUI but for now we will use cmd

subprocess.Popen(["cmd"], shell=True)

#all channels:
systemChannel = 1233588735115919381
#set up the bot

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# i just set the ranks to numbers to make it easy to use them in the code/bot
#ranks:

ranks = {
    "Martian": 9,
    "Big Cheese": 9,
    "General": 7,
    "Colonel": 6,
    "Major": 5,
    "Captain": 4,
    "Lieutenant": 3,
    "Sergeant": 2,
    "Private": 1,
    "Viewonly": 0,
}

rank_commands = {
    "Martian": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    "Big Cheese": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    "General": [7, 6, 5, 4, 3, 2, 1, 0],
    "Colonel": [6, 5, 4, 3, 2, 1, 0],
    "Major": [5, 4, 3, 2, 1, 0],
    "Captain": [4, 3, 2, 1, 0],
    "Lieutenant": [3, 2, 1, 0],
    "Sergeant": [2, 1, 0],
    "Private": [1, 0],
    "Viewonly": [0]
}

#members ranks:

martain_id = 267360288913883136
Big_Cheese_id = [745262479009120266, 1225272276979810386] # i have my alt account here too

# rank function:

def get_rank(member):
    if member.id == martain_id:
        return ranks["Martian"]
    elif member.id in Big_Cheese_id:
        return ranks["Big Cheese"]
    
def can_use_command(rank, command):
    allowed_commands = rank_commands.get(rank, [])
    return command in allowed_commands

# fetch commands:

def fetch_commands():
    try:
        response = requests.get("")
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch commands:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching commands:", e)
        return []

async def execute_commands(commands):
    for command in commands:
        command_type = command.get('type')
        if command_type == 'say':
            try:
                channel_id = int(command.get('channel_id'))
            except ValueError:
                print("Invalid channel ID:", command.get('channel_id'))
                continue  # Skip to the next command

            message = command.get('message')
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(message)
            else:
                print("Channel not found.")

# Commands:

@bot.command(name="list", description="to list all commands")
async def _list(ctx):
    command_list = [command.name for command in bot.commands]
    embed = discord.Embed(title="Available Commands", color=discord.Colour.blue())
    embed.description = "\n".join(command_list)
    await ctx.send(embed=embed)

@bot.command(name="post", guild_only=True)
async def _post(ctx):
    await ctx.send("This command is not ready for use yet")
    # want to and way for use put in a code to test the command but not rn 

@bot.command(name="restart", guild_only=False)
async def _Restart(ctx):
    required_rank = [8,9]
    author_rank = get_rank(ctx.author)

    if author_rank in required_rank:
        global bot_restarted
        bot_restarted = True
        await ctx.send("Restarting...")
        server_directory = os.path.join(os.getcwd(), "server")
        subprocess.run(["python", "restart.py"])
    else:
        await ctx.send("you Don't have permission to use this command")

@bot.command(name="Fetch&Excute")
async def fetch_and_execute(ctx):
    commands = fetch_commands()
    await execute_commands(commands)
    await ctx.send("Fetched and Execute")

# on ready code:

@bot.event
async def on_ready():
    print("Bot is online and ready. System now Operational.")
    await asyncio.sleep(2) # Wait 2 seconds
    channel = bot.get_channel(systemChannel)
    if channel:
        await channel.send("Bot is online and ready. System now Operational.")

# bot run code:
bot.run(TOKEN)