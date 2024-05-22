from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext.commands import Bot, check
import message_maker
import role_util
import json_load_edit as jle
import fulgens_main_db as db

# Helper Class
## Class for streamlined coloured console output
class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: discord.Intents = discord.Intents.default()
intents.message_content = True
bot: Bot = Bot(intents=intents, command_prefix="/")

# Commands
@bot.slash_command()
async def ping(interaction):
    print(f"{C.WARNING}LOG:{C.ENDC} Bot has been pinged")
    await interaction.respond(f"Pong! ({round(bot.latency * 1000)}ms)")
    
@bot.slash_command()
@check(role_util.check_for_role_hierarchy)
async def purge(interaction):
    print(f"{C.WARNING}LOG:{C.ENDC} Purge Command has been called: {C.OKBLUE}{interaction.channel.name}{C.ENDC}")
    await interaction.channel.purge()
    await interaction.respond(f'Channel has been purged.')

@bot.slash_command()
@check(role_util.check_for_role_hierarchy)
async def add_ban_channel(interaction):
    db.add_ban_channel(interaction)
    await interaction.respond(f'Channel was added to ban channels. Users that write a message in here will be banned automatically.')

@bot.slash_command()
@check(role_util.check_for_role_hierarchy)
async def set_log_channel(interaction):
    db.set_log_channel(interaction)
    await interaction.respond(f'Channel was set as logging channel. Notifications about updates and bans will be sent here.')

### Panda Den Only Commands

#TODO: Check should not raise an Exception OR handle it better. It works, it's just not pretty
@bot.slash_command(guild_ids=[356965153616429057])
@check(role_util.check_for_whitelisted_roles)
async def rights(interaction):
    print(f"{C.WARNING}LOG:{C.ENDC} Rights Check Command has been called")
    await interaction.respond(f"Rights have been checked")

@bot.slash_command(guild_ids=[356965153616429057])
@check(role_util.check_for_whitelisted_roles)
async def print_file(interaction, to_print: str):
    if to_print.lower() == 'rules':
        i_channel = interaction.channel
        await interaction.respond(f'Printing Rules')
        await i_channel.send(file=discord.File('img/WelcomeBanner.png'))
        await i_channel.send(embed=message_maker.rules_welcome_embed())
        await i_channel.send(file=discord.File('img/RolesAndChannelsBanner.png'))
        await i_channel.send(embed=message_maker.rules_roles_embed())
        await i_channel.send(file=discord.File('img/RulesBanner.png'))
        await i_channel.send(embed=message_maker.rules_rules_embed())
        return
    await interaction.respond(f'Couldn\'t Print')

@bot.slash_command(guild_ids=[356965153616429057])
@check(role_util.check_for_whitelisted_roles)
async def edit(interaction, file: str, key1: str, key2: str = ""):
        # check if it is a lowest level string
        # accept a new value
    print(f"{C.WARNING}LOG:{C.ENDC} Edit Command has been called: {C.OKBLUE}{file}{C.ENDC}, {C.OKBLUE}{key1}{C.ENDC}, {C.OKBLUE}{key2}{C.ENDC}.")
    await interaction.respond(f'This command is not implemented yet. WIP\nBut we were able to retrieve this string:\n{jle.read_string(file, key1, key2)}')
    
@bot.slash_command(guild_ids=[356965153616429057])
@check(role_util.check_for_whitelisted_roles)
async def backup(interaction, file):
    if jle.backup_json(file) == 'ERROR':
        await interaction.respond(f'ERROR: The file you were trying to backup does not exist.')
        return
    await interaction.respond(f'The file \"{file}.json\" was succesfully backed up to \"{file}_backup.json\".')

# Startup
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running.')

# Handling Messages
@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    guild_id = message.guild.id
    ban_channel = db.get_ban_channel_by_guild_id(guild_id)
    message_channel_id = message.channel.id

    if message_channel_id in ban_channel:
        # Comments are for production / test code swapping
        await message.delete()
        await message.author.ban(delete_message_days=1, reason=f'Using the Bot Bait Channel - We will assume that, since you used this channel this account was compromised or a bot.\nIf you believe this was an error, contact Elohim.\nMessage in question:\n{message.content}')
        
        log_id = db.get_log_channel_by_guild_id(guild_id)
        if log_id == None:
            log_channel = bot.get_channel(int(message_channel_id))
            await log_channel.send("You have no Log Channel set in your server. Consider setting it up with /set_log_channel.")
        else: 
            log_channel = bot.get_channel(int(log_id))
        print(log_channel)
        await log_channel.send(embed=message_maker.ban_embed(message.author, message.content, bot.get_channel(message_channel_id)))
        return

bot.run(TOKEN)