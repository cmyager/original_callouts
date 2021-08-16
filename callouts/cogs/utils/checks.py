import discord

############################################################################################################################
def is_event(message):
    """Check if a message contains event data"""
    if len(message.embeds) > 0:
        embed = message.embeds[0]
        return (message.channel.name == 'upcoming-events'
                and embed.fields
                and embed.fields[0]
                and embed.fields[1]
                and embed.fields[2]
                and embed.fields[0].name == "Time"
                and embed.fields[1].name.startswith("__Accepted")
                and embed.fields[2].name.startswith("__Declined__"))

############################################################################################################################
def is_raid(message):
    """ Check if a message contains raid data """
    if len(message.embeds) > 0:
        embed = message.embeds[0]
        if embed.author:
            return embed.author.name.startswith("Raid:")
        else:
            return False

############################################################################################################################
def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

############################################################################################################################
def is_private_channel(channel):
    if isinstance(channel, discord.abc.PrivateChannel):
        return True

############################################################################################################################
def is_event_create_message(message):
    is_message = False
    if message.author.name == "Callouts" and "to create an event." in message.content:
        # if message.author.name == "Callouts" and message.content == "React to this message to create an event.":
        is_message = True
    return is_message

############################################################################################################################
def purge_event_message(message):
    # create_message = is_event_create_message(message)
    # is_event_message = is_event(message)
    purge_message = True
    if is_event_create_message(message) or is_event(message):
        purge_message = False
    return purge_message
