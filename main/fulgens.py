from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

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
        await message.author.ban(delete_message_days=1, reason=f"Using the Bot Bait Channel - We will assume that, since you used this channel this account was compromised or a bot. Message in question:\n{user_message}")
    elif channel == "botcommands":
        # do nothing so far
        return
    else:
        return

# Main Entry Point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()