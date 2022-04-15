import os

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

BOT_TOKEN = os.environ.get('BOT_TOKEN', None)

bot = commands.Bot(command_prefix='$')


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


bot.run(BOT_TOKEN)
