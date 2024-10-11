import discord as dis
from discord.ext import commands, tasks
import os
import json
import asyncio
import time

# Set up intents (if your bot needs specific intents, you can enable them here)
intents = dis.Intents.default()
last_command_time = None

# Define constants
FILE_ERROR = "ERROR: File 010"
CONFIG_FILE = "default.json"

# Default config in case the file doesn't exist or fails to load
default_config = {
    "default_channel_id": 1233588735115919381,
    "Owners_ids": [1225272276979810386],
    "allowed_debug_user_id": None,
    "prefix": "$",
    "welcome_channel_id": None,
    "mod_log_channel_id": None,
    "OfflineTimer": 10,  # minutes
    "Bot_Token": None,
    "first_Time": True,
    "debug_mode": False
}

# Function to load config from the file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)  # Correctly load JSON file
    else:
        print(FILE_ERROR)
        return default_config  # Return default config if file doesn't exist

# Load the configuration
config = load_config()

# Get bot token from environment variable, config file, or default
def get_BotToken():
    token = os.getenv("DISCORD_BOT_TOKEN")  # Check environment variable first
    if not token:
        token = config.get("Bot_Token")  # Fallback to config file token
        if not token:
            print("ERROR: Bot token is missing in both environment variables and config file.")
            return None
    return token

# Get the prefix (fallback to default "$" if not found in config)
def get_prefix():
    return config.get("prefix", default_config['prefix']) 

# Get the welcome channel ID (fallback to None if not set in config)
def get_welcome_channel_id():
    return config.get("welcome_channel_id", None)

# Get the mod log channel ID (fallback to None if not set in config)
def get_mod_log_channel_id():
    return config.get("mod_log_channel_id", None)

# Get the allowed debug user ID (fallback to None if not set in config)
def get_allowed_debug_user_id():
    return config.get("allowed_debug_user_id", None)

# Get the default channel ID (fallback to None if not set in config)
def get_default_channel_id():
    return config.get("default_channel_id", None)

# Initialize the bot with the prefix from config or fallback to default
bot = commands.Bot(command_prefix=get_prefix(), intents=intents)

# Your bot's commands go here
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Start the bot using the token from either environment variable or config file
bot_token = get_BotToken()
if bot_token:
    bot.run(bot_token)
else:
    print("Bot cannot start without a valid token.")
