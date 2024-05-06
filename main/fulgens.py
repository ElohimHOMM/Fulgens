from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Message, File
from discord.ext.commands import Bot, check
import message_maker
import role_util
import discord
from json_load_edit import backup_json

# Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
bot: Bot = Bot(intents=intents, command_prefix="fulgens!")

# Startup
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running.')

# Commands
@bot.command(desc="Returns a Pong with the Bots latency", help="Returns a Pong with the Bots latency")
async def ping(ctx):
    print("Bot has been pinged")
    await ctx.send(f"Pong! ({round(bot.latency * 1000)}ms)")

#TODO: Check should not raise an Exception OR handle it better. It works, it's just not pretty
@bot.command()
@check(role_util.check_for_whitelisted_roles)
async def rights(ctx):
    await ctx.send(f"Rights have been checked")

@bot.command()
@check(role_util.check_for_whitelisted_roles)
async def print(ctx, to_print):
    if to_print == 'rules':
        await ctx.channel.send(file=File('img/WelcomeBanner.png'))
        await ctx.channel.send(embed=message_maker.rules_welcome_embed())
        await ctx.channel.send(file=File('img/RolesAndChannelsBanner.png'))
        await ctx.channel.send(embed=message_maker.rules_roles_embed())
        await ctx.channel.send(file=File('img/RulesBanner.png'))
        await ctx.channel.send(embed=message_maker.rules_rules_embed())

@bot.command()
@check(role_util.check_for_whitelisted_roles)
async def edit(ctx, file: str, key1: str, key2: str = ""):
    await ctx.channel.send(f'This command is not implemented yet. WIP')

@bot.command()
@check(role_util.check_for_whitelisted_roles)
async def purge(ctx):
    await ctx.channel.purge()

@bot.command()
@check(role_util.check_for_whitelisted_roles)
async def backup(ctx, file):
    if backup_json(file) == 'ERROR':
        await ctx.channel.send(f'ERROR: The file you were trying to backup does not exist.')
        return
    await ctx.channel.send(f'The file \"{file}.json\" was succesfully backed up to \"{file}_backup.json\".')


# Handling Messages
@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    logs = bot.get_channel(int(os.getenv('LOGS_CHANNEL')))
    bot_bait = bot.get_channel(int(os.getenv('BOT_BAIT_CHANNEL')))

    if channel == "bot-bait":
        # Comments are for production / test code swapping
        await message.author.ban(delete_message_days=1, reason=f'Using the Bot Bait Channel - We will assume that, since you used this channel this account was compromised or a bot.\nIf you believe this was an error, contact Elohim.\nMessage in question:\n{user_message}')
        await message.delete()
        await logs.send(embed=message_maker.ban_embed(username, user_message, bot_bait))
        #await mod_bot_communication.send(embed=message_maker.ban_embed(username, user_message, bot_bait))
        return
    
    await bot.process_commands(message)

# Main Entry Point
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()