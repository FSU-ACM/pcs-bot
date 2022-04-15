#import discord
from discord.ext import commands
import logging


logging.basicConfig(level=logging.DEBUG)
'''
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
'''

bot = commands.Bot(command_prefix='$')


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def clear_announcements(ctx, channel_id):
    guild = ctx.guild.get_channel(channel_id)
    print(guild)
    # channel.send('In announcements')

    await ctx.send(guild)

bot.run('OTYxNTEzMzk4MTUwMDA0ODA2.Yk6FIg.Xs74GaW6h5pf2B2Qgb1_c9YKEy4')
