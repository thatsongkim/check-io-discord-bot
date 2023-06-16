import discord
from discord.ext import commands
from datetime import datetime

import config
from channel import set_voice_channel, set_message_channel, get_channels

prefix = "/"
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


@bot.command(name="commands")
async def commands(ctx):
    await ctx.send(f"**{prefix}set -v <voice_channel_name>**: set voice channel\n"
                   f"**{prefix}set -m <message_channel_name>**: set message channel\n"
                   f"**{prefix}clear -v**: clear voice channel\n"
                   f"**{prefix}clear -m**: clear message channel\n"
                   f"**{prefix}clear -all**: clear all channels")


@bot.command(name="set")
async def set_channel(ctx, flag, channel_name):
    guild_id = ctx.guild.id
    if flag == "-v":
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            voice_channel_id = channel.__getattribute__("id")
            set_voice_channel(guild_id, voice_channel_id)
            await ctx.send(f"Voice channel set to {channel_name}")
        else:
            await ctx.send(f"Channel {channel_name} not found")
    elif flag == "-m":
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            message_channel_id = channel.__getattribute__("id")
            set_message_channel(guild_id, message_channel_id)
            await ctx.send(f"Message channel set to {channel_name}")
        else:
            await ctx.send(f"Channel {channel_name} not found")


@bot.command(name="clear")
async def clear(ctx, flag):
    guild_id = ctx.guild.id
    if flag == "-v":
        set_voice_channel(guild_id, 0)
        await ctx.send("Voice channel cleared")
    elif flag == "-m":
        set_message_channel(guild_id, 0)
        await ctx.send("Message channel cleared")
    elif flag == "-all":
        set_voice_channel(guild_id, 0)
        set_message_channel(guild_id, 0)
        await ctx.send("All channels cleared")


def time_string():
    return f"at **{datetime.now().strftime('%H:%M')}**"


def check_in_out_message(is_check_in, member):
    green_circle = ":green_circle:"
    red_circle = ":red_circle:"
    return f"{green_circle if is_check_in else red_circle} **{member}** {time_string()}"


@bot.event
async def on_voice_state_update(member, before, after):
    guild_id = member.guild.id
    channels = get_channels(guild_id)
    message_channel_id = channels["message_channel_id"]
    voice_channel_id = channels["voice_channel_id"]
    message_channel = discord.utils.get(member.guild.channels, id=message_channel_id)
    before_channel_id = before.channel.__getattribute__("id") if before.channel else None
    after_channel_id = after.channel.__getattribute__("id") if after.channel else None
    if before.channel is None and after_channel_id == voice_channel_id:
        await message_channel.send(check_in_out_message(True, member.display_name))
    elif before_channel_id == voice_channel_id and after.channel is None:
        await message_channel.send(check_in_out_message(False, member.display_name))


bot.run(config.get("TOKEN"))
