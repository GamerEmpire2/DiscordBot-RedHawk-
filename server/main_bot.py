import discord
from discord.ext import commands
import os
from dotenv import load_dotenv # when using the restart command it errors here after the restart.py calls this file
import asyncio
import subprocess
import requests
import random
import string
import mysql
import mysql.connector
import config
import requests
import re
import argparse
from argparse import ArgumentParser

Debug_mode = False

def process_arguments():
    global Debug_mode

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Turn on debug mode")

    # Add a flag argument for Debug mode
    parser.add_argument(
        "--debugON",            # The argument name
        action="store_true",    # This makes it a flag (boolean)
        help="Enable debug mode"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Check if the --debugON flag was provided
    if args.debugON:
        Debug_mode = True

    # Output for debugging purposes
    print(f"Debug mode: {Debug_mode}")

# Call the function to process arguments
process_arguments()

# Example usage in your bot
if Debug_mode:
    print("Debug mode is active.")
else:
    print("Debug mode is not active.")

# this will be your GUI but for now we will use cmd

# subprocess.Popen(["cmd"], shell=True)

#all channels:
systemChannel = 1233588735115919381
Normal_Channels = [1208180496555708477, 1233588735115919381]
#set up the bot

pythonPath = "venv\\scripts\\python.exe"
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot_restarted = None
DataBasepassword = os.getenv("DATABASE")
DataBase_user = os.getenv("DATABASEUSER")
FILE_NAME_PATTERN = r'file_V(\d+\.\d+\.\d+)\.txt'

bot = commands.Bot(command_prefix='$', intents=intents)

# i just set the ranks to numbers to make it easy to use them in the code/bot
#ranks:

ranks = {
    10: "Martian",
    9: "Big Cheese",
    7: "General",
    6: "Colonel",
    5: "Major",
    4: "Captain",
    3: "Lieutenant",
    2: "Sergeant",
    1: "Private",
    0: "Viewonly",
    -1: "Baned",
}

rank_commands = {
    "Martian": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    "Big Cheese": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    "General": [7, 6, 5, 4, 3, 2, 1, 0],
    "Colonel": [6, 5, 4, 3, 2, 1, 0],
    "Major": [5, 4, 3, 2, 1, 0],
    "Captain": [4, 3, 2, 1, 0],
    "Lieutenant": [3, 2, 1, 0],
    "Sergeant": [2, 1, 0],
    "Private": [1, 0],
    "Viewonly": [0],
    "Baned": [-1]
}


#members ranks:

martain_id =  1225272276979810386 #Tony's
Big_Cheese_id =  267360288913883136 # EMU
General_id = 409125766563889152 #Piano cat
Colonel_id = [957362142418456627, ] #the other admirtals of a braich

# rank function:

def get_rank(member):

    if member.id == martain_id:
        return 9
    elif member.id in Big_Cheese_id:
        return 9
    elif member.id in General_id:
        return 7
        print(get_rank)
    elif member.id in Colonel_id:
        return 6

def memebr_rank(ctx):
    if ctx.author.id == martain_id:
        return "Martian"
    elif ctx.author.id in Big_Cheese_id:
        return "Big_Cheese"
    elif ctx.author.id in General_id:
        return "Gerneral"
        print(memebr_rank)
    elif ctx.author.id in Colonel_id:
        return "Colonel"
    else:
        for rank, commands in rank_commands.items():
            if ctx.author.id in commands:
                return ranks[rank]
        return "unknown"
    
def Get_latest_version(files):
    version_files = {}
    for file in files:
        match = re.match(FILE_NAME_PATTERN, file['name'])
        if match:
            version = tuple(map(int, match.group(1).split('.')))
            version_files[version] = file['downnload_url']

    if version_files:
        lastest_version = max(version_files.keys())
        return version_files[lastest_version], lastest_version
    return None, None
        
def rank_level(ctx):
    rank = memebr_rank(ctx)
    if rank == "Martian":
        return 9
    elif rank == "Big_Cheese":
        return 9
    elif rank == "General":
        return 7
        print(rank_level)
    elif rank == "Colonel":
        return 6
    elif rank == "unknow":
        return -1
    return -2 # -2 is for unknow

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

            message = command.get("message")
            channel = bot.get_channel(channel_id)
            
            if Debug_mode and not message:
                message = "The Bot is in [DEBUG] mode"
            
            if channel and message:
                await channel.send(message)
            else:
                if not channel:
                    print("Channel not found")
                if not message:
                    print("Message is empty")

def store_token(discord_id, token):
    db = mysql.connector.connect(
        host="sql105.infinityfree.com",
        user=DataBase_user,
        password=DataBasepassword,
        database="if0_36069910_token_keep"
    )
    cursor = db.cursor()

    # Store the token with the associated Discord ID
    cursor.execute("REPLACE INTO user_tokens (discord_id, token) VALUES (%s, %s)", (discord_id, token))
    db.commit()
    cursor.close()
    db.close()

#-------------------------------------------------
#                   Commands:
#-------------------------------------------------

@bot.command(name="list", description="to list all commands")
async def _list(ctx):
    commands = [command.name for command in bot.commands]
    pages = []
    for i in range(0, len(commands), 8):
        page_commands = commands[i:i + 8]
        embed = discord.Embed(title="Available Commands", color=discord.Colour.blue())
        embed.description = "\n".join(page_commands)
        pages.append(embed)

    current_page = 0
    message = await ctx.send(embed=pages[current_page])

    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                current_page += 1
                await message.edit(embed=pages[current_page])
            elif str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await message.edit(embed=pages[current_page])

            await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            break

@bot.command(name="Ban", guild_only=True)
async def _Ban(ctx: commands.Context, user_id: int):
    try:
        user = await ctx.bot.fetch_user(user_id)
        user_rank_level = rank_level(ctx)
        
        if user_rank_level == "-2":
            await ctx.send("Your rank is unknown. Please DM Tony or EMU for code help or DM PianoCat for a rank if you already have a rank.")
        elif user_rank_level == "-1":
            await ctx.author.send("You are banned. Please DM PianoCat for more info.")
        else:
            if user_rank_level in [9, 8, 7]:
                guild = ctx.guild
                if guild is None:
                    await ctx.send("This command can only be used in a guild.")
                    return
                
                member = guild.get_member(user.id)
                if member:
                    await member.ban(reason="Banned by Pinaocat, or Bot Makers (Tony or EMU)")
                    await ctx.send(f"User {user.name} has been banned.")
                else:
                    await ctx.send(f"User with ID {user_id} is not a member of this guild.")
            else:
                await ctx.author.send("You can't use this command.")
    except discord.NotFound:
        await ctx.send(f"User with ID {user_id} was not found.")
    except discord.Forbidden:
        await ctx.send("I do not have permission to ban members.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command(name="timeout", guild_only=True)
async def _timeout(member):
    return

@bot.command(name="post", guild_only=True)
async def _post(ctx):
    await ctx.send("This command is not ready for use yet")
    # want to and way for use put in a code to test the command but not rn 

@bot.command(name="restart", guild_only=False)
async def _Restart(ctx):
    required_rank = [9, 8, 7]
    author_rank = get_rank(ctx.author)

    if author_rank in required_rank:
        global bot_restarted
        bot_restarted = True
        await ctx.send("Restarting...")
        server_directory = os.path.join(os.getcwd(), "server")
        subprocess.run([pythonPath, "server\\restart.py"])
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
        user_rank_name = user_ranks[user_id]
        user_rank_level = ranks.get(user_rank_name)
    else:
        user_rank_name = memebr_rank(ctx)
        user_rank_level = rank_level(ctx)
        print(user_rank_level)
        
    if user_rank_level is not None:
       
        # Create and send embed
        
        embed = discord.Embed(title="Rank Information", description=f"User: {ctx.author.mention}", color=0x00ff00)
        embed.add_field(name="Rank", value=user_rank_name, inline=False)
        embed.add_field(name="Rank Level", value=user_rank_level, inline=False)
        await ctx.send(embed=embed)

@bot.command(name="Verify_Database")
async def _check_database(ctx):
    required_rank = [9, 8, 7, 6]
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
        # Store the token in the database
        store_token(str(ctx.author.id), token)
        # Send the token via DM
        await ctx.author.send(f"Your token: {token}")
    else:
        await ctx.send("You don't have permission to use this command")


@bot.command(name="ViewRank", guild_only=True)
async def _see_rank(ctx, user_id: int):
    required_rank = [9, 8, 7, 6]
    author_rank = rank_level(ctx)  # Assuming rank_level function works for author

    if author_rank not in required_rank:
        await ctx.send("You don't have permission to use this command", ephemeral=True)
        return

    guild = ctx.guild
    member = guild.get_member(user_id)
    if member is None:
        await ctx.send("User not found", ephemeral=True)
        return
    
    if user_id in user_ranks:
        user_rank_name = user_ranks[user_id]
        user_rank_level = ranks.get(user_rank_name, "Unknown")
    else:
        user_rank_name = memebr_rank(ctx)  # Correct spelling
        user_rank_level = rank_level(ctx)

    embed = discord.Embed(title="User Rank Information", color=discord.Color.blue())
    embed.add_field(name="User", value=member.display_name, inline=False)
    embed.add_field(name="Rank Title", value=user_rank_name, inline=False)
    embed.add_field(name="Rank Level", value=user_rank_level, inline=False)
    await ctx.send(embed=embed)

class BotControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name="Shutdown")
    async def shutdown(self, ctx):
        required_rank = [9, 8, 7]
        author_rank = get_rank(ctx.author)

        if author_rank not in required_rank:
            await ctx.send("You don't have permission to use this command", ephemeral=True)
            return

        await ctx.send("Shutting down...")
        await self.bot.logout()

    intents = discord.Intents.default()
    intents.all()

@bot.command(name="BotV")
async def _BotV(ctx):
    try:
        respone = requests.get()
        respone.raise_for_satus()
        files = respone.json()

        download_url, lates_version = Get_latest_version(files)
        if download_url:
            file_response = requests.get(download_url)
            file_response.raise_for_status()

            with open('latest_file.txt', 'w') as file:
                file.write(file_response.txt)

            await ctx.send(f"file updated successfully to V{".".join(map(str, lates_version))}")
        else:
            await ctx.send("No versioned files found in the repository.")

    except requests.exceptions.RequestException as e:
        await ctx.send(f"Failed to fetch the file from GitHub: {e}")
    
process_arguments()

# on ready code:
@bot.event
async def on_ready():
    message = None

    if bot_restarted:
        message = "Bot restarted"
    elif Debug_mode:
        debug_channel = bot.get_channel(systemChannel)
        if debug_channel:
            await debug_channel.send("Debug Mode On, Only this channel will see this message")
            intents.members = True
    else:
        message = "Bot is online and ready. System now Operational"
        intents.members = True

    print(message)

    for channel_id in Normal_Channels:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)

# bot run code:
bot.add_cog(BotControl(bot))
bot.run(TOKEN)