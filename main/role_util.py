from discord import Member
from discord.ext.commands import Context

admin_roles = [423130072795578378, 460950936236457986, 543193353496297472, 493364519851261952]

def check_for_whitelisted_roles(ctx: Context):
    print("Rights Check has been called")
    member = ctx.author
    for role in member.roles:
        if role.id in admin_roles:
            return True
    return False

def check_for_role_hierarchy(ctx: Context):
    print("Hierarchy check has been called")
    bot_member: Member = ctx.guild.get_member(ctx.bot.user.id)
    return ctx.author.top_role > bot_member.top_role