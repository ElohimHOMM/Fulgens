from discord import Embed

def ban_embed(username, message, channel) -> Embed:
    embedVar = Embed(title="User banned", description=f"After a message in {channel.mention} the user {username} was banned.\nTheir messages have been deleted.")
    embedVar.add_field(name="Username", value = username)
    embedVar.add_field(name="Message for which they were banned", value = message)
    return embedVar