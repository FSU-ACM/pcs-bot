from multiprocessing.connection import wait
from discord.ext import commands
from discord import Intents, utils
import discord
import logging
import os


def get_secret(key, default=None):
    value = os.getenv(key, default)
    if value and os.path.isfile(value):
        with open(value) as f:
            return f.read().strip()
    return value

intents = Intents(messages=True, guilds=True, members=True)

'''
    EMAIL:
        TODO: 1. Verify email from discord user.

    ANNOUNCEMENTS
        TODO: 1. Clear all messages from pc-announcements channel

    LFG COMMANDS:
        1. Remove LFG Role from single user
        2. Remove LFG Role from multiple users
        3. Remove LFG Role from ALL users
        4. Clear all messages from LFG channel
        TODO: 5. After clone, move channel to top of list

    COMMANDS RESTRICTIONS
        1. Role, channel
        2. Verify permissions, delete message if wrong permissions
'''
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

BOT_TOKEN = get_secret('BOT_TOKEN', None)
GUILD_TOKEN = get_secret('GUILD_TOKEN', None)

LOWER = "LFG_Lower"
UPPER = "LFG_Upper"

UPPER_CHANNEL = "lfg-upper-division"
LOWER_CHANNEL = "lfg-lower-division"

# ''' Tokens for LFG Roles '''
# LOWER_TOKEN = os.environ.get('LOWER_TOKEN', None)
# UPPER_TOKEN = os.environ.get('UPPER_TOKEN', None)

''' Specify channel name to only allow commands to occur there'''
BOT_CHANNEL = get_secret('BOT_CHANNEL', "bot_commands")

def bot_channel_only():
    async def predicate(ctx):
        if ctx.channel.name != BOT_CHANNEL:
            # Do the handling here or in on_command_error handler
            message = ctx.message
            await message.delete()
            await ctx.send("You do not have permission to use these commands.")
            #raise commands.CheckFailure("Channel isn't valid!")
        return True

    return commands.check(predicate)



@bot.event
@bot_channel_only()
async def on_message(message):
    if message.author.bot:
        ctx = await bot.get_context(message)
 
        if ctx.valid:
            args = message.content.split(" ")

            if len(args) > 1:
                args  = args[1:]
            else:
                args = []

            await ctx.invoke(ctx.command, *args)
            


@bot_channel_only()
@bot.command()
async def test(ctx):
    await ctx.send(f'$help')

@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def help(ctx):
    """
    Overwrites default help command.
    """
    await ctx.send("This bot's commands are private!")


@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def clear(ctx, channel_id):
    """
    Clones channel with messages deleted, changes channel_ID

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
    if channel is not None:
        await channel.clone(reason="Has been nuked")
        await channel.delete()
    else:
        await ctx.send(f'No channel was found with id: **{channel_id}**')

@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def remove_all_roles(ctx):
    """
    """
    guild = bot.get_guild(int(GUILD_TOKEN))

    lower_role = utils.get(guild.roles, name=LOWER)
    upper_role = utils.get(guild.roles, name=UPPER)

    await lower_role.delete()
    await upper_role.delete()

@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def create_roles(ctx):
    """
    """
    guild = bot.get_guild(int(GUILD_TOKEN))
    await guild.create_role(name=UPPER)
    await guild.create_role(name=LOWER)

    # Slower than just getting by ID
    lfg_upper = utils.get(guild.text_channels, name=UPPER_CHANNEL)
    lfg_lower = utils.get(guild.text_channels, name=LOWER_CHANNEL)
    
    await lfg_upper.set_permissions(utils.get(guild.roles, name=UPPER), read_messages=True, send_messages=True)
    await lfg_lower.set_permissions(utils.get(guild.roles, name=LOWER), read_messages=True, send_messages=True)

@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def remove_role(ctx, user_ids, division):
    """
    Remove the LFG Roles from a User/list of Users, LFG_Upper or LFG_Lower role

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

    role = utils.get(guild.roles, name=division)
    # TODO: Error Checking  

    for u in user_ids: 
        user = guild.get_member_named(u)
        await user.remove_roles(role)

@bot_channel_only()
@bot.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def add_role(ctx, user_ids, division):
    """
    Add the LFG Roles to a User/List of Users, LFG_Upper or LFG_Lower

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
    print("userids: ", user_ids)

    role = utils.get(guild.roles, name=division)


    print("DIVISION: ", division)

    if division == UPPER:
        lfg_channel = utils.get(guild.text_channels, name=UPPER_CHANNEL)
    elif division == LOWER:
        lfg_channel = utils.get(guild.text_channels, name=LOWER_CHANNEL)
    else:
        404

    # TODO: Error Checking  

    for u in user_ids: 
        user = guild.get_member_named(u)
        await user.add_roles(role)
        await lfg_channel.send(f'**{user}** has joined, looking for a group!')

bot.run(BOT_TOKEN)
