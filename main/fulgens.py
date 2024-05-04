from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
import message_maker
import role_util

# Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Channels
logs = os.getenv('LOGS_CHANNEL')
mod_bot_communication = os.getenv('MOD_BOT_COMMUNICATION_CHANNEL')
bot_bait = os.getenv('BOT_BAIT_CHANNEL')

# Startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running.')

# Handling Messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    if channel == "bot-bait":
        # Comments are for production / test code swapping
        await message.author.ban(delete_message_days=1, reason=f'Using the Bot Bait Channel - We will assume that, since you used this channel this account was compromised or a bot.\nIf you believe this was an error, contact Elohim.\nMessage in question:\n{user_message}')
        await message.delete()
        await client.get_channel(logs).send(embed=message_maker.ban_embed(username, user_message, client.get_channel(bot_bait)))
        #await client.get_channel(mod_bot_communication).send(embed=message_maker.ban_embed(username, user_message, client.get_channel(bot_bait)))
    
    # check for prefix
    if not user_message.startswith('fulgens!') or not role_util.check_for_whitelisted_roles(message.author):
        return
    command = user_message[8:]
    print(f'command received: {command}')
    command_list = command.split(" ")
    command = command_list.pop(0)
    arguments = command_list
    if command == 'help':
        if len(arguments) == 0:
            await message.channel.send('Help command recognized. This is WIP')
    if command == 'print':
        if not len(arguments) == 1:
            await message.channel.send('The print command accepts exactly one arguments.')
            return
        if arguments[0] == 'rules':
            await message.delete()
            await message.channel.send(embed=message_maker.rules_welcome_embed())
            #await message.channel.send(embed=message_maker.rules_roles_embed())
            #await message.channel.send(embed=message_maker.rules_rules_embed())

# Main Entry Point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()