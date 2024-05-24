import discord
from discord.ext import commands
import os
import logging
import logger
import asyncio

systemChannel = 1233588735115919381
LOG_CHANNEL_ID = None

AuthUsers = {
    1:"1225272276979810386",
    2: "409125766563889152",
    3: "745262479009120266",
    4: "267360288913883136"
}

TOKEN2 = os.getenv("TOKEN2")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def not_authenticated(ctx):
    return "You Are Not Authenticated"

def get_rank(member):
    if str(member.id) == AuthUsers[1]:
        return 1
    elif str(member.id) == AuthUsers[2]:
        return 2
    elif str(member.id) == AuthUsers[3]:
        return 3
    elif str(member.id) == AuthUsers[4]:
        return 4
    else:
        return 0
        

@bot.command(name="set_log_channel")
async def _setlogchannel(ctx, channel: discord.TextChannel):
    author_rank = get_rank(ctx.author)
    if author_rank == [1, 2, 3, 4]:
        try:
            with open("text-files\\log_channels.txt", "a") as file:
                file.write(f"{channel.id}\n")
            await ctx.send(f"Log channel {channel.mention} added.")
        except IOError as e:
            await ctx.send(f"An error occurred while writing to the file: {str(e)}")
    else:
        await ctx.send(not_authenticated)

@bot.event
async def on_message(message):
    # Process commands
    await bot.process_commands(message)

    # Check if the message is from a bot or from the logging channel itself
    if message.author.bot or message.channel.id == LOG_CHANNEL_ID:
        return

    # Check if the message starts with the command prefix
    if message.content.startswith("$set_log_channel"):
        # Parse the command and get the arguments
        command_args = message.content.split()
        if len(command_args) == 2:
            # Get the channel mentioned in the command
            channel_id = int(command_args[1][2:-1])  # Extract the channel ID from the mention
            channel = bot.get_channel(channel_id)

            # Author rank check
            author_rank = get_rank(message.author)
            if author_rank in [1, 2, 3, 4]:
                try:
                    with open("text-files\\log_channels.txt", "a") as file:
                        file.write(f"{channel.id}\n")
                    await message.channel.send(f"Log channel {channel.mention} added.")
                except IOError as e:
                    await message.channel.send(f"An error occurred while writing to the file: {str(e)}")
            else:
                await message.channel.send(not_authenticated)
        await _setlogchannel(message)


@bot.event
async def on_message_log(message):
    # Check if the message is from a bot or from the logging channel itself
    if message.author.bot or message.channel.id == LOG_CHANNEL_ID:
        return

    # Create an embed for the log message
    embed = discord.Embed(
        title="Message Log",
        description=message.content,
        color=discord.Color.blue()
    )
    embed.set_author(name=message.author.name)
    embed.set_footer(text=f"Sent in #{message.channel.name}")

    # Fetch the logging channel
    if LOG_CHANNEL_ID is None:
        await message.channel.send("No log channel set. Please use $set_log_channel to set one or more.")
    else:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        # Send the embed to the logging channel
        await log_channel.send(embed=embed)

# Rename the event to avoid overriding the on_message event
bot.add_listener(on_message_log, "on_message")

@bot.event
async def on_ready():
    channel = bot.get_channel(systemChannel)
    if channel:
        await channel.send("logger bot is online")

bot.run(TOKEN2)