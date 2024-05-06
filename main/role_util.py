from discord import Member

admin_roles = [423130072795578378, 460950936236457986, 543193353496297472, 493364519851261952]

def check_for_whitelisted_roles(ctx):
    print("Rights Check has been called")
    member = ctx.author
    for role in member.roles:
        if role.id in admin_roles:
            return True
    return False