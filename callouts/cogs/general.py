from datetime import datetime

import discord
from discord.ext import commands, ipc
import psutil
import pytz

from cogs.utils.message_manager import MessageManager
from cogs.utils import constants

########################################################################################################################
class General(commands.Cog):

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        # self.channel_name = "welcome"

    ####################################################################################################################
    # @commands.command()
    # @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def countdown(self, ctx):
        """Show time until upcoming Destiny 2 releases"""
        manager = MessageManager(ctx)
        pst_now = datetime.now(tz=pytz.timezone('US/Pacific'))
        text = ""

        for name, date in constants.RELEASE_DATES:
            diff = date - pst_now
            days = diff.days + 1
            if days == 0:
                text += "{}: Today!\n".format(name)
            elif days == 1:
                text += "{}: Tomorrow!\n".format(name)
            elif days > 1:
                text += "{}: {} days\n".format(name, days)

        if not text:
            text = "There are no concrete dates for our next adventure..."

        countdown = discord.Embed(title="Destiny 2 Countdown", color=constants.BLUE)
        countdown.description = text
        await manager.send_embed(countdown)
        await manager.clean_messages()

    ####################################################################################################################
    @ipc.server.route()
    async def user_in_guild_ipc(self, data):
        return data.user_id in [user.id for user in self.bot.users]

    ####################################################################################################################
    @ipc.server.route()
    async def get_guilds_ipc(self, data):
        guilds = []
        for guild in self.bot.guilds:
            if data.user_id in [member.id for member in guild.members] and "Clan " in guild.name:
                guild_info = {}
                guild_info["id"] = guild.id
                guild_info["name"] = guild.name
                guild_info["users"] = {}
                for member in guild.members:
                    if member.bot is False:
                        user = {}
                        user["id"] = member.id
                        user["avatar_url"] = member.avatar_url._url.replace("?size=1024","?size=64")
                        guild_info["users"][member.display_name] = user
                guilds.append(guild_info)
        return guilds

    ####################################################################################################################
    @commands.command()
    @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def about(self, ctx):
        """Display information about the bot itself"""
        manager = MessageManager(ctx)
        e = discord.Embed(title='Callouts v{}'.format(constants.VERSION), colour=constants.BLUE)

        # e.set_author(name=str(owner))

        # statistics
        total_members = sum(1 for _ in self.bot.get_all_members())
        total_online = len({m.id for m in self.bot.get_all_members() if m.status is discord.Status.online})
        total_unique = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        e.add_field(name='Members', value='{} total\n{} unique\n{} unique online'.format(total_members, total_unique, total_online))
        e.add_field(name='Channels', value='{} total\n{} text\n{} voice'.format(text + voice, text, voice))

        memory_usage = "%0.2f" % (self.process.memory_full_info().uss / 1024**2)
        cpu_usage = "%0.2f" % (self.process.cpu_percent() / psutil.cpu_count())
        e.add_field(name='Process', value='{} MiB\n{}% CPU'.format(memory_usage, cpu_usage))

        e.add_field(name='Guilds', value=len(self.bot.guilds))
        e.add_field(name='Commands Run', value=self.bot.command_count)
        e.add_field(name='Uptime', value=self.get_bot_uptime(brief=True))

        e.set_footer(text='Made with discord.py', icon_url='http://i.imgur.com/5BFecvA.png')
        await manager.send_embed(e)
        await manager.clean_messages()

    ####################################################################################################################
    def get_bot_uptime(self, *, brief=False):
        now = datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    ####################################################################################################################
    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):
    #     welcome_channel = None
    #     for channel in guild.channels:
    #         if channel.name == self.channel_name:
    #             welcome_channel = channel
    #     """Send welcome message"""
    #     message = f"Greetings! My name is **{self.bot.user.name}**.\n\n"
    #     message += "**Command Prefix**\n"
    #     message += f"My default prefix is **!**, but you can also just mention me with **@{self.bot.user.name}**.\n"
    #     message += "For a list of all available commands, use the **!help** command. If you want more "
    #     message += "information on a command, use **!help <command_name>**.\n"
    #     await guild.owner.send(message)

    ####################################################################################################################
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     """If a reaction represents a user RSVP, update the DB and event message"""
    #     channel = self.bot.get_channel(payload.channel_id)

    #     if isinstance(channel, discord.abc.PrivateChannel):
    #         return
    #     try:
    #         message = await channel.fetch_message(payload.message_id)
    #     except Exception as E:
    #         print(E)
    #         return

    #     guild = channel.guild
    #     member = await guild.fetch_member(payload.user_id)
    #     deleted = None

        # # We check that the user is not the message author as to not count
        # # the initial reactions added by the bot as being indicative of attendance
        # if is_event(message) and member != message.author:
        #     title = message.embeds[0].title
        #     if payload.emoji.name == "\N{WHITE HEAVY CHECK MARK}":
        #         await self.set_attendance(member, guild, 1, title, message)
        #     elif payload.emoji.name == "\N{CROSS MARK}":
        #         await self.set_attendance(member, guild, 0, title, message)
        #     elif payload.emoji.name == "\N{WHITE QUESTION MARK ORNAMENT}":
        #         await self.set_attendance(member, guild, 2, title, message)
        #     elif payload.emoji.name == "\N{THUMBS UP SIGN}":
        #         user_info = self.bot.db.get_user_by_discord_id(member.id)
        #         await self.bot.cogs["Report"].get_report(user_info, guild=guild)
        #     elif payload.emoji.name == "\N{SKULL}":
        #         deleted = await self.delete_event(guild, title, member, channel)

        #     if not deleted:
        #         try:
        #             await message.remove_reaction(payload.emoji, member)
        #         except:
        #             pass
        # elif is_event_create_message(message) and member != message.author:
        #     await message.remove_reaction(payload.emoji, member)
        #     ctx = FCTX(channel, member, message, guild, self.bot)
        #     await self.event(ctx, deprecated=True)
