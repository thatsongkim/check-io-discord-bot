from datetime import datetime

import discord
from discord.ext import commands
import config

prefix = "/"
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

message_channel: discord.TextChannel
voice_channel = None


@bot.command(name="set")
async def set_channel(ctx, flag, channel_name):
    global message_channel
    global voice_channel
    if flag == "-v":
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            voice_channel = channel
            await ctx.send(f"Voice channel set to {channel_name}")
        else:
            await ctx.send(f"Channel {channel_name} not found")
    elif flag == "-m":
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            message_channel = channel
            await ctx.send(f"Message channel set to {channel_name}")
        else:
            await ctx.send(f"Channel {channel_name} not found")


def time_string():
    return f"at **{datetime.now().strftime('%H:%M')}**"


def check_in_out_message(is_check_in, member):
    green_circle = ":green_circle:"
    red_circle = ":red_circle:"
    return f"{green_circle if is_check_in else red_circle} **{member}** {time_string()}"


@bot.event
async def on_voice_state_update(member, before, after):
    global message_channel
    global voice_channel
    if before.channel is None and after.channel == voice_channel:
        await message_channel.send(check_in_out_message(True, member))
    elif before.channel == voice_channel and after.channel is None:
        await message_channel.send(check_in_out_message(False, member))


bot.run(config.get("TOKEN"))
