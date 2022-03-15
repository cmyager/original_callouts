from datetime import datetime, timedelta
from aioscheduler import TimedScheduler
import pytz
from discord.ext import commands, tasks, ipc
import discord
from collections import namedtuple
from db.query_wrappers import get_event_role, get_event_delete_role
from cogs.utils.message_manager import MessageManager
from cogs.utils.checks import is_event, is_int, is_event_create_message, purge_event_message
from cogs.utils import constants
from cogs.utils.format import format_role_name

FCTX = namedtuple('FCTX', ['channel', 'author', 'message', 'guild', 'bot'])

############################################################################################################################
class Events(commands.Cog):

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot
        self.channel_name = "upcoming-events"
        self.clean_channel.start()
        self.scheduler = TimedScheduler()

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.get_events_channel(guild=guild)
            await self.list_events(guild)
        self.scheduler.start()
        await self.setup_reminders()

    ####################################################################################################################
    @ipc.server.route()
    async def reload_events_ipc(self, data):
        for guild in self.bot.guilds:
            await self.get_events_channel(guild=guild)
            await self.list_events(guild)
        await self.setup_reminders()

    ####################################################################################################################
    @tasks.loop(hours=1.0)
    async def clean_channel(self):
        for guild in self.bot.guilds:
            event_channel = await self.get_events_channel(guild=guild)
            await event_channel.purge(limit=999, check=purge_event_message)

    ####################################################################################################################
    async def setup_reminders(self):
        reminder_times = [60, 45, 30, 15, 10, 5]

        # Cancel existing tasks
        while self.scheduler._next:
            self.scheduler.cancel(self.scheduler._next)

        # Setup new reminders for all events
        for guild in self.bot.guilds:
            for event in self.bot.db.get_events(guild.id):
                if event.get("utctime") and event.get("utctime") > datetime.utcnow():
                    for reminder_time in reminder_times:
                        # TODO MAKE MINUTES
                        event_reminder_time = event.get("utctime") - timedelta(minutes=reminder_time)
                        if event_reminder_time > datetime.utcnow():
                            self.scheduler.schedule(self.send_reminders(guild, event), event_reminder_time)

    ####################################################################################################################
    @clean_channel.before_loop
    async def before_clean_channel(self):
        await self.bot.wait_until_ready()

    ####################################################################################################################
    async def send_reminders(self, guild, event):
        event = self.bot.db.get_event(guild.id, event.get("event_title"))
        accepted = []
        confirmed = []
        max_members = event.get("max_members")
        if event.get("accepted"):
            accepted = event.get("accepted").split(",")
        if event.get("confirmed"):
            confirmed = event.get("confirmed").split(",")

        sent = len(confirmed)
        for user_id in [i for i in accepted if i not in confirmed]:
            standby = False
            if sent >= max_members and max_members > 0:
                standby = True
                # TODO: Accepted person getting standby if standby accepts
                standby = False
            user = guild.get_member(int(user_id))
            event_title = event.get("event_title")
            user_event = self.bot.db.get_user_event_attendance(user_id, guild.id, event_title)
            attempts = user_event.get("attempts")
            if attempts > 5:
                event_message = await self.get_event_message(guild, event_title)
                await self.set_attendance(user, guild, 0, event_title, event_message, confirmed=2)
                self.bot.db.add_user_event_attempt(user_id, guild.id, event_title, reset=True)
                await user.send("You have been removed from the event")
            else:
                event_reminder_embed = await self.create_event_reminder_embed(guild, event, attempts, standby)
                msg = await user.send(embed=event_reminder_embed)
                self.bot.db.add_user_event_attempt(user_id, guild.id, event_title)
                await msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                sent += 1

    ####################################################################################################################
    async def create_event_create_message(self, event_channel):
        msg = await event_channel.send("Visit https://theclanwithoutaplan.com to create an event.")
        await msg.add_reaction("\N{HEAVY PLUS SIGN}")

    ####################################################################################################################
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def event(self, ctx, deprecated=False):
        """
        Create an event in the events channel

        After invoking the event command, the bot will ask
        you to enter the event details. Once the event
        is created, it will appear in the upcoming-events
        channel. The upcoming-events channel is designed with
        the assumption that it isn't used for anything but
        displaying events; non event messages will be deleted.

        Users will be able to accept and decline the
        event by adding reactions. If a maximum number
        of attendees is set and the event is full,
        additional attendees will be placed in a standby
        section. If a spot opens up, the user at the
        top of the standby section will be automatically
        moved into the event.

        By default, everyone can make events. However, a minimum role
        requirement to create events can be defined in the settings.
        See `help settings seteventrole` for more information.

        The event creator and those with the Manage Sever permission
        can delete events by reacting to the event message with \U0001f480.
        """
        manager = MessageManager(ctx)
        event_role = get_event_role(ctx)
        #TODO
        _member_permissions = ctx.author.permissions_in(ctx.channel)

        if event_role:
            if ctx.author.top_role < event_role:
                #TODO
                _event_role_str = format_role_name(event_role)
                await manager.send_message("You must be of role **{}** or higher to do that.".format(event_role))
                return await manager.clean_messages()

        if deprecated is False:
        # await manager.send_message('Event creation instructions have been messaged to you')
            manager.add_messages_to_clean([ctx.message])
            await manager.clean_messages()
            return await manager.send_private_message("!event is not supported anymore. Please react to the pinned message in the upcoming-events channel to create an event.")

        # Title
        await manager.send_private_message("Enter event title:")
        res = await manager.get_next_private_message()
        if not res:
            return await manager.clean_messages()
        title = res.content

        # Description
        await manager.send_private_message("Enter event description (type 'none' for no description):")
        res = await manager.get_next_private_message()
        if not res:
            return await manager.clean_messages()
        if res.content.upper() != 'NONE':
            description = res.content
        else:
            description = ""

        # Number of attendees
        max_members = 0
        while not max_members:
            await manager.send_private_message("Enter the maximum numbers of attendees (type 'none' for no maximum):")
            res = await manager.get_next_private_message()
            if not res:
                return await manager.clean_messages()
            if res.content.upper() == 'NONE':
                break
            elif is_int(res.content) and int(res.content) in range(1,10000):
                max_members = int(res.content)
            else:
                await manager.send_private_message("Invalid entry. Must be a number between 1 and 9999.")

        # Start time
        start_time = None
        while not start_time:
            await manager.send_private_message("Enter event time (YYYY-MM-DD HH:MM AM/PM):")
            res = await manager.get_next_private_message()
            if not res:
                return await manager.clean_messages()
            start_time_format = '%Y-%m-%d %I:%M %p'
            try:
                start_time = datetime.strptime(res.content, start_time_format)
            except ValueError:
                await manager.send_private_message("Invalid event time!")

        # Time zone
        time_zone = None
        while not time_zone:
            await manager.send_private_message("Enter the time zone (PST, EST, etc):")
            res = await manager.get_next_private_message()
            if not res:
                return await manager.clean_messages()
            user_timezone = "".join(res.content.upper().split())
            if user_timezone not in constants.TIME_ZONES:
                await manager.send_private_message("Unsupported time zone")
            else:
                time_zone = user_timezone

        # UTC time
        utctime = datetime(1,1,1)

        if time_zone in constants.TIME_ZONE_CONVERT.keys():
            localtimezone = pytz.timezone(constants.TIME_ZONE_CONVERT[time_zone])
            local_dt = localtimezone.localize(start_time, is_dst=None)
            utctime = local_dt.astimezone(pytz.utc)

        # RSVP
        rsvp = None
        while rsvp is None:
            res = None
            await manager.send_private_message("Enter a list of usernames to add to the event or 'None'.\nExample: 'cmyager, Moners, Ivar'")
            res = await manager.get_next_private_message()
            if res:
                if res.content.upper() == "NONE":
                    rsvp = []
                else:
                    usernames = res.content.upper().split(",")
                    usernames = [i.strip() for i in usernames]
                    users = [i for i in ctx.guild.members if i.display_name.upper() in usernames]
                    userNameList = [i.display_name for i in users]
                    await manager.send_private_message(f"Does this look good? (Y/N)\n{', '.join(userNameList)}")
                    res = await manager.get_next_private_message()
                    if res:
                        if res.content.upper() in ["Y", "YES"]:
                            rsvp = users

        affected_rows = self.bot.db.create_event(title, start_time, time_zone, ctx.guild.id, description, max_members, ctx.author.id, utctime)
        if affected_rows == 0:
            await manager.send_private_message("An event with that name already exists!")
            return await manager.clean_messages()
        
        for member in rsvp:
            self.bot.db.add_user(member.id)
            self.bot.db.update_attendance(member.id, ctx.guild.id, 1, title, datetime.now(), 0)

        event_channel = await self.get_events_channel(ctx.guild)
        await manager.send_private_message("Event created! The " + event_channel.mention + " channel will be updated momentarily.")
        await self.list_events(ctx.guild)
        await self.setup_reminders()
        await manager.clean_messages()

    ####################################################################################################################
    @ipc.server.route()
    async def create_event_ipc(self, data):
        STATUS = "Unknown Error Occured"
        try:
            EVENT = data.event
            title = EVENT["event_title"]
            time_zone = 'US/Central'
            guild_id = EVENT["guild_id"]
            description = EVENT["description"]
            max_members = EVENT["max_members"]
            author_id = EVENT["author_id"]
            rsvp = EVENT["rsvp"]

            # Start Time
            start_time = datetime.strptime(EVENT["start_time"], '%Y-%m-%d %I:%M %p')

            # UTC time
            utctime = datetime(1,1,1)
            localtimezone = pytz.timezone(time_zone)
            local_dt = localtimezone.localize(start_time, is_dst=None)
            utctime = local_dt.astimezone(pytz.utc)
            
            affected_rows = self.bot.db.create_event(title, start_time, time_zone, guild_id, description, max_members, author_id, utctime)
            if affected_rows == 0:
                STATUS = "An event with that name already exists!"
            else:
                STATUS = "Event was created, but and error occured inviting people"
                for member_id in rsvp:
                    self.bot.db.add_user(member_id)
                    self.bot.db.update_attendance(member_id, guild_id, 1, title, datetime.now(), 0)
                STATUS = True
        except:
            pass
        finally:
            return {"status": STATUS}

    ####################################################################################################################
    def user_can_create_events(self, member):
        pass

    ####################################################################################################################
    async def list_events(self, guild):
        """Clear the event channel and display all upcoming events"""
        events_channel = await self.get_events_channel(guild)
        await events_channel.purge(limit=999, check=purge_event_message)
        events = self.bot.db.get_events(guild.id)
        db_titles = [i['event_title'] for i in events]
        msg_titles = []

        messages = await events_channel.history().flatten()
        for message in messages:
            if is_event_create_message(message):
                continue
            if is_event(message):
                title = message.embeds[0].title
                if title not in db_titles:
                    await message.delete()
                else:
                    msg_titles.append(title)

        to_create_titles = [i for i in db_titles if i not in msg_titles]
        if len(to_create_titles) > 0:
            for event in events:
                if event["event_title"] not in to_create_titles:
                    continue
                event_embed = await self.create_event_embed(guild, event)
                msg = await events_channel.send(embed=event_embed)
                await msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                await msg.add_reaction("\N{CROSS MARK}")
                await msg.add_reaction("\N{WHITE QUESTION MARK ORNAMENT}")

    ####################################################################################################################
    async def private_emoji_handler(self, channel, payload):
        message = await channel.fetch_message(payload.message_id)
        if message.embeds:
            embed = message.embeds[0]
            if "Event Reminder" in embed.title:
                if message.author.id != payload.user_id:
                    guild_name = embed.fields[0].value
                    event_name = embed.fields[1].value
                    guild = [i for i in self.bot.guilds if i.name == guild_name][0]
                    user = await guild.fetch_member(payload.user_id)
                    event_message = await self.get_event_message(guild, event_name)
                    if event_message:
                        if payload.emoji.name == "\N{WHITE HEAVY CHECK MARK}":
                            await self.set_attendance(user, guild, 1, event_name, event_message, confirmed=1)

    ####################################################################################################################
    async def get_event_message(self, guild, event_title):
        event_message = None
        events_channel = await self.get_events_channel(guild=guild)
        event_messages = await events_channel.history().flatten()
        for e_message in event_messages:
            if is_event(e_message) and e_message.embeds[0].title == event_title:
                event_message = e_message
        return event_message
    
    ####################################################################################################################
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """If a reaction represents a user RSVP, update the DB and event message"""
        channel = self.bot.get_channel(payload.channel_id)

        if isinstance(channel, discord.abc.PrivateChannel):
            await self.private_emoji_handler(channel, payload)
            return
        try:
            message = await channel.fetch_message(payload.message_id)
        except Exception as E:
            print(E)
            return

        guild = channel.guild
        member = await guild.fetch_member(payload.user_id)
        deleted = None

        # We check that the user is not the message author as to not count
        # the initial reactions added by the bot as being indicative of attendance
        if is_event(message) and member != message.author:
            title = message.embeds[0].title
            if payload.emoji.name == "\N{WHITE HEAVY CHECK MARK}":
                await self.set_attendance(member, guild, 1, title, message)
            elif payload.emoji.name == "\N{CROSS MARK}":
                await self.set_attendance(member, guild, 0, title, message)
            elif payload.emoji.name == "\N{WHITE QUESTION MARK ORNAMENT}":
                await self.set_attendance(member, guild, 2, title, message)
            elif payload.emoji.name == "\N{THUMBS UP SIGN}":
                user_info = self.bot.db.get_user_by_discord_id(member.id)
                await self.bot.cogs["Report"].get_report(user_info, guild=guild)
            elif payload.emoji.name == "\N{SKULL}":
                deleted = await self.delete_event(guild, title, member, channel)

            if not deleted:
                try:
                    await message.remove_reaction(payload.emoji, member)
                except:
                    pass
        elif is_event_create_message(message) and member != message.author:
            await message.remove_reaction(payload.emoji, member)
            ctx = FCTX(channel, member, None, guild, self.bot)
            await self.event(ctx, deprecated=True)

    ####################################################################################################################
    async def set_attendance(self, member, guild, attending, title, message, confirmed=0):
        """Send updated event attendance info to db and update the event"""
        self.bot.db.add_user(member.id)
        self.bot.db.update_attendance(member.id, guild.id, attending, title, datetime.now(), confirmed)

        # Update event message in place for a more seamless user experience
        event = self.bot.db.get_event(guild.id, title)
        if event:
            event_embed = await self.create_event_embed(guild, event)
            await message.edit(embed=event_embed)
        else:
            raise ValueError("Could not retrieve event")

    ####################################################################################################################
    async def delete_event(self, guild, title, member, channel):
        """Delete an event and update the events channel on success"""
        event_delete_role = get_event_delete_role(self.bot, guild)
        result = self.bot.db.get_event_creator(guild.id, title)
        creator_id = result.get('user_id') if result else None

        if member.permissions_in(channel).manage_guild or (member.id == creator_id) or (event_delete_role and member.top_role >= event_delete_role):
            deleted = self.bot.db.delete_event(guild.id, title)
            if deleted:
                await self.list_events(guild)
                await self.setup_reminders()
                return True
        else:
            try:
                await member.send("You don't have permission to delete that event.")
            except:
                pass

    ####################################################################################################################
    async def get_events_channel(self, guild):
        """Return the events channel if it exists, otherwise create one and return it"""
        event_channel = None
        for channel in guild.channels:
            if channel.name == self.channel_name:
                event_channel = channel

        if event_channel is None:
            # Need to make sure the bot can still send messages in the events channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=True),
                guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True)
            }
            event_channel = await guild.create_text_channel(self.channel_name, overwrites=overwrites)
        
        # check if the create event message is posted
        event_create_message_exists = False
        async for message in event_channel.history():
            if is_event_create_message(message):
                event_create_message_exists = True
                break
        if event_create_message_exists is False:
            await self.create_event_create_message(event_channel)
        return event_channel

    ####################################################################################################################
    async def create_event_reminder_embed(self, guild, event, attempt, standby=False):
        event_embed = await self.create_event_embed(guild, event)
        event_embed.set_footer(text=f"React to this message to confirm your attendance.\nAttempt {attempt}/5")
        title = event_embed.title
        time = event_embed.fields[0]
        event_embed.title = "Event Reminder"
        if standby is True:
            event_embed.title = f"{event_embed.title} (Standby)"
        event_embed.remove_field(4)
        event_embed.remove_field(3)
        event_embed.remove_field(2)
        event_embed.remove_field(1)
        event_embed.remove_field(0)
        event_embed.add_field(name="Server", value=guild.name, inline=False)
        event_embed.add_field(name="Event", value=title, inline=False)
        event_embed.add_field(name="Time", value=time.value, inline=False)
        return event_embed

    ####################################################################################################################
    async def create_event_embed(self, guild, event):
        """Create and return a Discord Embed object that represents an upcoming event"""
        title = event.get('event_title')
        description = event.get('description')
        time = event.get('start_time')
        timezone = event.get('timezone')
        creator_id = event.get('user_id')
        accepted = event.get('accepted')
        declined = event.get('declined')
        maybe = event.get('maybe')
        max_members = event.get('max_members')

        confirmed = []
        if event.get('confirmed'):
            confirmed = event.get('confirmed').split(",")

        rejected = []
        if event.get('rejected'):
            rejected = event.get('rejected').split(",")

        embed_msg = discord.Embed(color=constants.BLUE)
        embed_msg.title = title

        creator = await guild.fetch_member(creator_id)
        message = "React with {} to remove this event".format('\U0001f480')
        message += "\nReact with {} to get the raid report (WIP)".format('\U0001F44D')
        if creator:
            message = f"Created by {creator.display_name}\n{message}"
        embed_msg.set_footer(text=message)

        if description:
            embed_msg.description = description
        time_str = time.strftime("%A %b %-d, %Y @ %-I:%M %p")
        embed_msg.add_field(name="Time", value=time_str + " " + timezone, inline=False)

        if accepted:
            accepted_list = None
            if max_members:
                accepted_list = accepted.split(',')[:max_members]
            else:
                accepted_list = accepted.split(',')
            text = ""
            for user_id in accepted_list:
                member = await guild.fetch_member(int(user_id))
                if member:
                    member_name = member.display_name
                    if user_id in confirmed:
                        member_name = f"**{member_name}**"
                    text += f"{member_name}\n"
                if not text:
                    text = '-'
            if max_members:
                embed_msg.add_field(name="__Accepted ({}/{})__".format(len(accepted_list), max_members), value=text)
            else:
                embed_msg.add_field(name="__Accepted__", value=text)
        else:
            if max_members:
                embed_msg.add_field(name="__Accepted (0/{})__".format(max_members), value="-")
            else:
                embed_msg.add_field(name="__Accepted__", value="-")

        if declined:
            declined_list = declined.split(',')
            text = ""
            for user_id in declined_list:
                member = await guild.fetch_member(int(user_id))
                if member:
                    member_name = member.display_name
                    if user_id in rejected:
                        member_name = f"~~{member_name}~~"
                    text += f"{member_name}\n"
            if not text:
                text = '-'
            embed_msg.add_field(name="__Declined__", value=text)
        else:
            embed_msg.add_field(name="__Declined__", value="-")

        if maybe:
            maybe_list = maybe.split(',')
            text = ""
            for user_id in maybe_list:
                member = await guild.fetch_member(int(user_id))
                if member:
                    text += "{}\n".format(member.display_name)
            if not text:
                text = '-'
            embed_msg.add_field(name="__Maybe__", value=text)
        else:
            embed_msg.add_field(name="__Maybe__", value="-")

        if accepted and max_members:
            standby_list = accepted.split(',')[max_members:]
            if standby_list:
                text = ""
                for user_id in standby_list:
                    member = await guild.fetch_member(int(user_id))
                    if member:
                        member_name = member.display_name
                        if user_id in confirmed:
                            member_name = f"**{member_name}**"
                        text += f"{member_name}\n"
                    if not text:
                        text = '-'
                embed_msg.add_field(name="__Standby__", value=text, inline=False)

        return embed_msg
