from discord import Member

admin_roles = [423130072795578378, 460950936236457986, 543193353496297472, 493364519851261952]

def check_for_whitelisted_roles(member: Member):
    for role in admin_roles:
        if role in member.roles:
            return True
    return False