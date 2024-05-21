from discord import Embed, Member
import json_load_edit as jle

def ban_embed(user: Member, message, channel) -> Embed:
    embed_var: Embed = Embed(title="User banned", description=f"After a message in {channel.mention} the user {user.name} was banned.\nTheir messages have been deleted.")
    embed_var.add_field(name="Username", value = user.name)
    embed_var.add_field(name="User ID", value = user.id)
    embed_var.add_field(name="Message for which they were banned", value = message)
    return embed_var

def rules_welcome_embed() -> Embed:
    payload = jle.get_payload("rules")
    welcome_message = payload.get("welcome-message")
    embed_var = Embed(description=welcome_message)
    return embed_var

def rules_roles_embed() -> Embed:
    payload = jle.get_payload("rules")
    generic_roles = payload.get("generic-roles")
    self_assign_roles = payload.get("self-assign-roles")
    channels_intro = payload.get("channels-intro")
    channels = payload.get("channels")
    media_channels = payload.get("media-channels")
    gallery_channels = payload.get("gallery-channels")
    network_channels = payload.get("network-channels")
    special_channels = payload.get("special-channels")

    embed_var: Embed = Embed()
    embed_var.add_field(name="Roles:", value=get_embed_list(generic_roles))
    embed_var.add_field(name="Self assign Roles:", value=get_embed_list(self_assign_roles))
    embed_var.add_field(name="", value="")
    channel_string = channels_intro + get_embed_list(channels, "#")
    embed_var.add_field(name="Channels:", value=channel_string)
    embed_var.add_field(name="Media Channels:", value=get_embed_list(media_channels, "#"))
    embed_var.add_field(name="Gallery Channels:", value=get_embed_list(gallery_channels, "#"))
    embed_var.add_field(name="Network Channels:", value=get_embed_list(network_channels, "#"))
    embed_var.add_field(name="Special Channels:", value=get_embed_list(special_channels, "#"))
    return embed_var

def get_embed_list(list, prefix = "") -> str:
    desc: str = ""
    for line in list:
        desc += f"**{prefix}{line}**: {list.get(line)}\n"
    return desc

def rules_rules_embed() -> Embed:
    payload = jle.get_payload("rules")
    counter: int = 0
    rules = payload.get("rules")
    rule_ending = payload.get("rule-ending")

    embed_var: Embed = Embed()
    for rule in rules:
        counter += 1
        embed_var.add_field(name="", value=f"{counter}. {rule}\n")
    embed_var.add_field(name="", value=rule_ending)
    return embed_var