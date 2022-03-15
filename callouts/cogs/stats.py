from discord.ext import commands
import discord

import pydest

from cogs.utils.message_manager import MessageManager
from cogs.utils import constants, helpers
from cogs.embed_builders import pvp_stats_embed, pve_stats_embed
from cogs.models.pvp_stats import PvPStats
from cogs.models.pve_stats import PvEStats

############################################################################################################################
class Stats(commands.Cog):

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot

    ####################################################################################################################
    @commands.group()
    @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def stats(self, ctx):
        """Display various Destiny 2 stats"""
        if ctx.invoked_subcommand is None:
            cmd = self.bot.get_command('help')
            await ctx.invoke(cmd, 'stats')

    ####################################################################################################################
    @stats.command()
    async def pvp(self, ctx):
        """Display PvP stats across all characters on your account

        `stats pve` - Display your PvP stats (preferred platform)
        """
        user_info = await self.get_user_info(ctx)
        platform_info = self.get_primary_account_info(user_info)

        platform = platform_info["platform"]
        platform_id = platform_info["platform_id"]
        bungie_name = platform_info["platform_username"]

        manager = MessageManager(ctx)
        await ctx.channel.trigger_typing()

        pvp_stats_json = await self.get_stats(platform, platform_id, [5])

        if not pvp_stats_json:
            await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
            return await manager.clean_messages()

        pvp_stats = PvPStats(pvp_stats_json['allPvP']['allTime'])
        await manager.send_embed(pvp_stats_embed(pvp_stats, "Crucible Stats", bungie_name, platform))
        await manager.clean_messages()

    ####################################################################################################################
    @stats.command()
    async def pve(self, ctx):
        """Display PvE stats across all characters on your account

        `stats pve` - Display your PvE stats (preferred platform)
        """
        user_info = await self.get_user_info(ctx)
        platform_info = self.get_primary_account_info(user_info)

        platform = platform_info["platform"]
        platform_id = platform_info["platform_id"]
        bungie_name = platform_info["platform_username"]

        manager = MessageManager(ctx)
        await ctx.channel.trigger_typing()

        pve_stats_json = await self.get_stats(platform, platform_id, [7,4,16,17,18,46,47])
        if not pve_stats_json:
            await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
            return await manager.clean_messages()

        pve_stats = PvEStats(pve_stats_json)
        await manager.send_embed(pve_stats_embed(pve_stats, bungie_name, platform))
        await manager.clean_messages()

    ####################################################################################################################
    @stats.command()
    async def trials(self, ctx):
        """Display Trials stats across all characters on your account

        `stats trials` - Display your PvE stats (preferred platform)"""
        user_info = await self.get_user_info(ctx)
        platform_info = self.get_primary_account_info(user_info)

        platform = platform_info["platform"]
        platform_id = platform_info["platform_id"]
        bungie_name = platform_info["platform_username"]

        manager = MessageManager(ctx)
        await ctx.channel.trigger_typing()

        trials_stats_json = await self.get_stats(platform, platform_id, [84])
        if not trials_stats_json:
            await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
            return await manager.clean_messages()

        trials_stats = PvPStats(trials_stats_json['trials_of_osiris'].get('allTime'))
        await manager.send_embed(pvp_stats_embed(trials_stats, "Trials of Osiris Stats", bungie_name, platform))
        await manager.clean_messages()

    @stats.command()
    async def ib(self, ctx):
        """Display Iron Banner stats across all characters on your account

        `stats ib` - Display your Iron Banner stats (preferred platform)
        """
        user_info = await self.get_user_info(ctx)
        platform_info = self.get_primary_account_info(user_info)

        platform = platform_info["platform"]
        platform_id = platform_info["platform_id"]
        bungie_name = platform_info["platform_username"]

        manager = MessageManager(ctx)
        await ctx.channel.trigger_typing()

        ib_stats_json = (await self.get_stats(platform, platform_id, [19]))['ironBanner'].get('allTime')
        if not ib_stats_json:
            await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
            return await manager.clean_messages()

        ib_stats = PvPStats(ib_stats_json)
        await manager.send_embed(pvp_stats_embed(ib_stats, "Iron Banner Stats", bungie_name, platform))
        await manager.clean_messages()

    ####################################################################################################################
    # @stats.command()
    # async def rumble(self, ctx, username=None, platform=None):
    #     """Display Rumble stats across all characters on an account

    #     In order to use this command for your own account, you must first register your Destiny 2
    #     account with the bot via the register command.

    #     `stats rumble` - Display your Rumble stats (preferred platform)
    #     \$`stats rumble clayton_yager ps` - Display clayton_yager's Rumble stats on PlayStation
    #     \$`stats rumble @user` - Display a registered user's Rumble stats (preferred platform)
    #     \$`stats rumble @user pc` - Display a registered user's Rumble stats on Steam
    #     """
    #     manager = MessageManager(ctx)
    #     await ctx.channel.trigger_typing()

    #     # Get membership details. This depends on whether or not a platform or username were given.
    #     membership_details = await helpers.(self.bot, ctx, username, platform)

    #     # If there was an error getting membership details, display it
    #     if isinstance(membership_details, str):
    #         await manager.send_message(membership_details)
    #         return await manager.clean_messages()
    #     else:
    #         platform_id, membership_id, bungie_name = membership_details

    #     rumble_stats_json = (self.get_stats(platform, platform_id, [48]))['rumble'].get('allTime')
    #     if not rumble_stats_json:
    #         await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
    #         return await manager.clean_messages()

    #     rumble_stats = PvPStats(rumble_stats_json)
    #     await manager.send_embed(pvp_stats_embed(rumble_stats, "Rumble Stats", bungie_name, platform_id))
    #     await manager.clean_messages()


    # @stats.command()
    # async def doubles(self, ctx, username=None, platform=None):
    #     """Display Doubles stats across all characters on an account

    #     In order to use this command for your own account, you must first register your Destiny 2
    #     account with the bot via the register command.

    #     `stats doubles` - Display your Doubles stats (preferred platform)
    #     \$`stats doubles clayton_yager ps` - Display clayton_yager's Doubles stats on PlayStation
    #     \$`stats doubles @user` - Display a registered user's Doubles stats (preferred platform)
    #     \$`stats doubles @user pc` - Display a registered user's Doubles stats on Steam
    #     """
    #     manager = MessageManager(ctx)
    #     await ctx.channel.trigger_typing()

    #     # Get membership details. This depends on whether or not a platform or username were given.
    #     membership_details = await helpers.(self.bot, ctx, username, platform)

    #     # If there was an error getting membership details, display it
    #     if isinstance(membership_details, str):
    #         await manager.send_message(membership_details)
    #         return await manager.clean_messages()
    #     else:
    #         platform_id, membership_id, bungie_name = membership_details

    #     doubles_stats_json = (self.get_stats(platform, platform_id, [49]))['allDoubles'].get('allTime')
    #     if not doubles_stats_json:
    #         await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
    #         return await manager.clean_messages()

    #     doubles_stats = PvPStats(doubles_stats_json)
    #     await manager.send_embed(pvp_stats_embed(doubles_stats, "Doubles Stats", bungie_name, platform_id))
    #     await manager.clean_messages()


    # @stats.command()
    # async def mayhem(self, ctx, username=None, platform=None):
    #     """Display Mayhem stats across all characters on an account

    #     In order to use this command for your own account, you must first register your Destiny 2
    #     account with the bot via the register command.

    #     `stats mayhem` - Display your Mayhem stats (preferred platform)
    #     \$`stats mayhem clayton_yager ps` - Display clayton_yager's Mayhem stats on PlayStation
    #     \$`stats mayhem @user` - Display a registered user's Mayhem stats (preferred platform)
    #     \$`stats mayhem @user pc` - Display a registered user's Mayhem stats on Steam
    #     """
    #     manager = MessageManager(ctx)
    #     await ctx.channel.trigger_typing()

    #     # Get membership details. This depends on whether or not a platform or username were given.
    #     membership_details = await helpers.(self.bot, ctx, username, platform)

    #     # If there was an error getting membership details, display it
    #     if isinstance(membership_details, str):
    #         await manager.send_message(membership_details)
    #         return await manager.clean_messages()
    #     else:
    #         platform_id, membership_id, bungie_name = membership_details

    #     mayhem_stats_json = (self.get_stats(platform, platform_id, [25]))['allMayhem'].get('allTime')
    #     if not mayhem_stats_json:
    #         await manager.send_message("Sorry, I can't seem to retrieve those stats right now")
    #         return await manager.clean_messages()

    #     mayhem_stats = PvPStats(mayhem_stats_json)
    #     await manager.send_embed(pvp_stats_embed(mayhem_stats, "Mayhem Stats", bungie_name, platform_id))
    #     await manager.clean_messages()

    ####################################################################################################################
    async def get_user_info(self, ctx):
        user_info = self.bot.db.get_user_by_discord_id(ctx.author.id)
        if not user_info:
            # Get the user registered
            user_info = await self.bot.cogs["Register"].register(ctx)
        return user_info

    ####################################################################################################################
    def get_primary_account_info(self, user_info):
        platform_id = None
        platform_username = None
        platform = user_info.get("platform")
        if platform == 1:
            platform_id = user_info.get('xbox_id')
            platform_username = user_info.get('xbox_name')
        elif platform == 2:
            platform_id = user_info.get('psn_id')
            platform_username = user_info.get('psn_name')
        elif platform == 3:
            platform_id = user_info.get('steam_id')
            platform_username = user_info.get('steam_name')
        elif platform == 5:
            platform_id = user_info.get('stadia_id')
            platform_username = user_info.get('stadia_name')
        return {"platform_id": platform_id,
                "platform_username": platform_username,
                "platform": platform}

    ####################################################################################################################
    async def get_stats(self, platform_id, membership_id, modes):
        try:
            res = await self.bot.destiny.api.get_historical_stats(platform_id, membership_id, groups=['general'], modes=modes)
        except:
            return
        if res['ErrorCode'] == 1:
            return res['Response']
