import discord
from botutils import has_prefix, get_content_without_prefix

def __get_valid_roles(config, message, names):
    val = []
    for role in message.guild.roles:
        low = role.name.lower()
        if low in names and low in config['valid_roles']:
            val.append(role)
    return val

async def handle(client, config, message):
    if not has_prefix(config, message):
        return

    content = get_content_without_prefix(config, message)
    potential_roles = content.split()

    if potential_roles[0] != 'giveroles':
        return

    message.channel.typing()

    if len(message.author.roles) > 1:
        await message.channel.send('You already have a role.')
        return    

    roles = [x.lower() for x in potential_roles[1:]]

    role_objects = __get_valid_roles(config, message, roles)
    if len(role_objects) > 0:
        await message.author.add_roles(*role_objects)
        await message.channel.send('Roles added: %s' % ', '.join(map(lambda x: x.name, role_objects)))
    else:
        await message.channel.send('No valid roles specified')
