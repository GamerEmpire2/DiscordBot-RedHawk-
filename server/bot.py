import discord
from discord.ext import commands
import os
import dotenv # when using the restart command it errors here after the restart.py calls this file
import asyncio
import subprocess
import requests
import random
import string

# this will be your GUI but for now we will use cmd

# subprocess.Popen(["cmd"], shell=True)

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

def read_ranks(file_path):
    ranks = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma and check if there are enough values
            parts = line.strip().split(',')
            if len(parts) != 2:
                print(f"Ignoring invalid line: {line.strip()}")
                continue
            
            # If there are enough values, unpack them
            user_id, rank_name = parts
            ranks[int(user_id)] = rank_name
    return ranks

user_ranks = read_ranks('text-files\\UserRanks.txt')

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
        subprocess.run(["python", "server\\restart.py"])
    else:
        await ctx.send("you Don't have permission to use this command")

@bot.command(name="Fetch&Excute")
async def fetch_and_execute(ctx):
    commands = fetch_commands()
    await execute_commands(commands)
    await ctx.send("Fetched and Execute")

@bot.command(name="Check_Rank")
async def check_rank(ctx):
    # Get user's ID
    user_id = ctx.author.id
    
    # Check if user's ID exists in user_ranks
    if user_id in user_ranks:
        # Get the user's rank from the user_ranks dictionary
        user_rank_name = user_ranks[user_id]
        user_rank_level = ranks.get(user_rank_name)
    else:
        # If user's rank is not found in user_ranks, use the get_rank function
        user_rank_name = get_rank(ctx.author)
        user_rank_level = ranks.get(user_rank_name)
        
    if user_rank_level is not None:
        # Create and send embed with rank information
        embed = discord.Embed(title="Rank Information", description=f"User: {ctx.author.mention}", color=0x00ff00)
        embed.add_field(name="Rank", value=user_rank_name, inline=False)
        embed.add_field(name="Rank Level", value=user_rank_level, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Your rank level is unknown.")
        
    # Create and send embed
    embed = discord.Embed(title="Rank Information", description=f"User: {ctx.author.mention}", color=0x00ff00)
    embed.add_field(name="Rank", value=user_rank_name, inline=False)
    embed.add_field(name="Rank Level", value=user_rank_level, inline=False)  # Add rank level to embed
    await ctx.send(embed=embed)

@bot.command(name="Verify_Database")
async def _check_database(ctx):
    required_rank = [9, 8, 7]
    author_rank = get_rank(ctx.author)

    if author_rank in required_rank:
        databaste_path = "./discordbot.db"
        if os.path.isfile(databaste_path):
            await ctx.send("Database is available")
        else:
            await ctx.send("Database is not available")
    else:
        await ctx.send("You dont have permission to use this command")

@bot.command(name="DashBoard")
async def _get_token(ctx):
    required_rank = [9, 8, 7]
    author_rank = get_rank(ctx.author)

    if author_rank in required_rank:
        # Generate a random token
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        # Send the token via DM
        await ctx.author.send(f"Your token: {token}")
    else:
        await ctx.send("You dont have permission to use this command")

@bot.command(name="ViewRank", guild_only=True)
async def _see_rank(ctx):
    required_rank = [9, 8, 7]
    author_rank = get_rank(ctx.author)

    if author_rank in required_rank:
        await ctx.send("command is comming soon")
    else:
        await ctx.send("You dont have permission to use this command", ephemeral=True)

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