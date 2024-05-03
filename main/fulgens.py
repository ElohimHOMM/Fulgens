from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
import message_maker

# Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Channels
logs = 1235889759646388274
mod_bot_communication = 1235894297577127977
bot_bait = 1235887929767759893

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
    if not user_message.startswith('fulgens!'):
        return
    command = user_message[8:]
    print(f'command received: {command}')
    command = command.split(" ")
    arguments = command[1:]
    command = command[0]
    if command == 'help':
        if not len(arguments) == 0:
            await message.channel.send('The help command doesn\'t accept any arguments.')
            return
        await message.channel.send('')


# Commands
#if channel == "mod-bot-communication":
    #    ## These Commands only work when sent to the mod-bot-communication Channel. They for example: update rules
    #    if message.
    #elif channel == "rules":

# Main Entry Point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()