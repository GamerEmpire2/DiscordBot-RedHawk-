import discord
from discord.ext import commands
import os
import logging
import server.logger_bot as logger_bot
import asyncio

systemChannel = 1233588735115919381
LOG_CHANNEL_ID = None

AuthUsers = {
    1: "1225272276979810386",
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


def log_file():
    return ".\\server\\log_channels.txt"


@bot.command(name="set_log_channel")
async def _setlogchannel(ctx, channel: discord.TextChannel):
    author_rank = get_rank(ctx.author)
    if author_rank in [1, 2, 3, 4]:
        try:
            with open(log_file(), 'w') as file:
                file.write(f"{channel.id}\n")
            global LOG_CHANNEL_ID
            LOG_CHANNEL_ID = channel.id
            await ctx.send(f"Log channel {channel.mention} added.")
        except IOError as e:
            await ctx.send(f"An error occurred while writing to the file: {str(e)}")
    else:
        await ctx.send(not_authenticated(ctx))


@bot.event
async def on_message(message):
    # Process commands
    await bot.process_commands(message)

    # Check if the message is from a bot or from the logging channel itself
    if message.author.bot or message.channel.id == LOG_CHANNEL_ID:
        return

    # Log message
    await on_message_log(message)


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
        await message.channel.send("No log channel set. Please use $set_log_channel to set one.")
    else:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            # Send the embed to the logging channel
            await log_channel.send(embed=embed)


@bot.event
async def on_ready():
    global LOG_CHANNEL_ID
    if LOG_CHANNEL_ID == None:
        LOG_CHANNEL_ID = 1240158663004389467
    else:
        return LOG_CHANNEL_ID

    channel = bot.get_channel(systemChannel)
    if LOG_CHANNEL_ID == 1240158663004389467:
        await channel.send("Error: Bot log channel file read failure. Default bot log channel ID: 1240158663004389467. For assistance, please direct message Tony or EMU.")
    else:
        await channel.send("Logger bot is online")

bot.run(TOKEN2)