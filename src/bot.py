import os

#import discord
from discord.ext import commands
from discord import Intents
import logging

intents = Intents(messages=True, guilds=True, members=True)

'''
    ANNOUNCEMENTS
        1. Clear all messages from pc-announcements channel

    LFG COMMANDS:
        1. Remove LFG Role from single user
        2. Remove LFG Role from multiple users
        TODO: 3. Remove LFG Role from ALL users
        4. Clear all messages from LFG channel

    COMMANDS RESTRICTIONS
        1. TODO: Role, channel
        2. TODO: Verify permissions, delete message if wrong permissions
'''

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

bot = commands.Bot(command_prefix='$', intents = intents)

BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
GUILD_TOKEN = os.environ.get('GUILD_TOKEN', None)

''' Tokens for LFG Roles '''
LOWER_TOKEN = os.environ.get('LOWER_TOKEN', None)
UPPER_TOKEN = os.environ.get('UPPER_TOKEN', None)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def clear(ctx, channel_id):
    """
    Clear all messages in a given channel

    Syntax:
        $clear <channel_id> 
    
    Parameters:
        ctx : Context Class Object
            Represents the context in which a command is being invoked under.
        channel_id : string (converted to int for functions)
            ID of channel to have messages deleted. 
            Get ID from Discord Server, Right-click Channel, Copy ID

    """
    channel = bot.get_channel(int(channel_id))
    msgs = [message async for message in channel.history()]
    await channel.delete_messages(msgs)

@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def remove_role(ctx, user_ids, division):
    """
    Remove the LFG Roles from Users, LFG_Upper or LFG_Lower

    Syntax:
        $remove_role <user_ids> <"LFG_Lower"/"LFG_Upper"> 
    
    Parameters:
        ctx : Context Class Object
            Represents the context in which a command is being invoked under.
        user_ids: comma separated string, converted to List
            List of comma separate user IDS to remove the LFG role from.
            Format of User ID : Name#1234
        division : String
            Determine which role to remove, either LFG_Upper or LFG_Lower
            
    """
    guild = bot.get_guild(int(GUILD_TOKEN))
    user_ids = list(user_ids.split(','))

    if division == "LFG_Lower":
        role = guild.get_role(int(LOWER_TOKEN))
    elif division == "LFG_Upper":
        role = guild.get_role(int(UPPER_TOKEN))
    else:        
        role = 404

    for u in user_ids: 
        user = guild.get_member_named(u)
        await user.remove_roles(role)

@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def add_role(ctx, user_ids, division):
    """
    Add the LFG Roles to Users, LFG_Upper or LFG_Lower

    Syntax:
        $add_role <user_ids> <"LFG_Lower"/"LFG_Upper"> 
    
    Parameters:
        ctx : Context Class Object
            Represents the context in which a command is being invoked under.
        user_ids: comma separated string, converted to List
            List of comma separate user IDS to add the LFG role to.
            Format of User ID : Name#1234
        division : String
            Determine which role to add, either LFG_Upper or LFG_Lower
            
    """
    guild = bot.get_guild(int(GUILD_TOKEN))
    user_ids = list(user_ids.split(','))

    if division == "LFG_Lower":
        role = guild.get_role(int(LOWER_TOKEN))
    elif division == "LFG_Upper":
        role = guild.get_role(int(UPPER_TOKEN))
    else:        
        role = 404

    for u in user_ids: 
        user = guild.get_member_named(u)
        await user.add_roles(role)

bot.run(BOT_TOKEN)