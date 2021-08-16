from discord.ext import commands, tasks
import discord
import asyncio

from cogs.utils import constants
from cogs.utils.message_manager import MessageManager

############################################################################################################################
class Core(commands.Cog):
    """Core functionality required for the bot to function"""

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot
        self.channel_name = "bot-commands"
        self.clean_channel.start()

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_ready(self):
        self.display_startup_info()
        self.add_remove_offline_guilds()
        for guild in self.bot.guilds:
            await self.get_commands_channel(guild)

    ####################################################################################################################
    @tasks.loop(hours=1.0)
    async def clean_channel(self):
        for guild in self.bot.guilds:
            command_channel = await self.get_commands_channel(guild=guild)
            async for message in command_channel.history():
                await message.delete()

    ####################################################################################################################
    @clean_channel.before_loop
    async def before_clean_channel(self):
        await self.bot.wait_until_ready()

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_member_remove(self, user):
        """Remove user from database when they leave the guild"""
        member_ids = []
        for member in self.bot.get_all_members():
            member_ids.append(member.id)

        if user.id not in member_ids:
            self.bot.db.remove_user(user.id)

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Command error handler"""
        manager = MessageManager(ctx)

        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.MissingRequiredArgument):
            pass

        elif isinstance(error, commands.NotOwner):
            pass

        elif isinstance(error, commands.NoPrivateMessage):
            await manager.send_message("You can't use that command in a private message")

        elif isinstance(error, commands.CheckFailure):
            await manager.send_message("You don't have the required permissions to do that")

        elif isinstance(error, commands.CommandOnCooldown):
            await manager.send_message(error)

        # Non Discord.py errors
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, discord.errors.Forbidden):
                pass
            elif isinstance(error.original, asyncio.TimeoutError):
                await manager.send_private_message("I'm not sure where you went. We can try this again later.")
            else:
                raise error

        else:
            raise error

        await manager.clean_messages()

    ####################################################################################################################
    def add_remove_offline_guilds(self):
        """Add/remove guilds that may have added/removed the bot while it was offline"""
        to_delete = []
        results = self.bot.db.get_guilds()

        for row in results:
            guild_id = row.get('guild_id')
            guild = self.bot.get_guild(guild_id)
            if not guild:
                to_delete.append(guild_id)

        for guild_id in to_delete:
            self.bot.db.remove_guild(guild_id)

    ####################################################################################################################
    def display_startup_info(self):
        print('Callouts v{}'.format(constants.VERSION))
        print('Username: {}'.format(self.bot.user.name))
        print('------')

    ####################################################################################################################
    async def get_commands_channel(self, guild):
        """Return the events channel if it exists, otherwise create one and return it"""
        for channel in guild.channels:
            if channel.name == self.channel_name:
                return channel

        # Need to make sure the bot can still send messages in the events channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=True, add_reactions=True),
            guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True)
        }
        return await guild.create_text_channel(self.channel_name, overwrites=overwrites, topic="Run bot commands in this channel.")

