from discord import Embed
import json

def ban_embed(username, message, channel) -> Embed:
    embed_var = Embed(title="User banned", description=f"After a message in {channel.mention} the user {username} was banned.\nTheir messages have been deleted.")
    embed_var.add_field(name="Username", value = username)
    embed_var.add_field(name="Message for which they were banned", value = message)
    return embed_var

def rules_welcome_embed() -> Embed:
    with open('main/rules.json') as file:
        payload: dict = json.load(file)
    welcome_message = payload.get("welcome-message")
    embed_var = Embed(description=welcome_message)
    embed_var.set_image("img/WelcomeBanner.png")
    return embed_var