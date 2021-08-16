from datetime import datetime

from discord.ext import commands
import discord

from db.query_wrappers import get_event_role, get_event_delete_role
from cogs.utils.message_manager import MessageManager
from cogs.utils.checks import is_raid
from cogs.utils import constants
from cogs.utils.format import format_role_name

# from cogs.raid_models.scourge import ScourgeModel
from cogs.raid_models.deepstone import DeepStoneModel
from cogs.raid_models.vault import VaultModel

RAIDS = {
    # ScourgeModel().name: ScourgeModel,
    DeepStoneModel().name: DeepStoneModel,
    VaultModel().name: VaultModel
}

class Raid(commands.Cog):

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot

    ####################################################################################################################
    @commands.group()
    @commands.guild_only()
    @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def raid(self, ctx):
        """
        Display in-depth raid info
        """
        if ctx.invoked_subcommand is None:
            cmd = self.bot.get_command('help')
            await ctx.invoke(cmd, 'raid')

    ####################################################################################################################
    async def raid_base(self, ctx, model):
        manager = MessageManager(ctx)
        manager.add_messages_to_clean([ctx.message])
        await ctx.channel.trigger_typing()
        await manager.clean_messages()

        raid_embed = await self.create_raid_embed(model)
        msg = await manager.send_embed(raid_embed)
        await self.add_reactions(msg, model)

    ####################################################################################################################
    # @raid.command()
    # async def scourge(self, ctx):
    #     '''Provides information on encounters in The Scourge of the Past raid'''
    #     await self.raid_base(ctx, ScourgeModel())

    ####################################################################################################################
    @raid.command()
    async def deepstone(self, ctx):
        '''Provides information on encounters in The Deep Stone Crypt raid'''
        await self.raid_base(ctx, DeepStoneModel())

    ####################################################################################################################
    @raid.command()
    async def vault(self, ctx):
        '''Provides information on encounters in The Deep Stone Crypt raid'''
        await self.raid_base(ctx, VaultModel())

    ####################################################################################################################
    async def add_reactions(self, msg, model):
        for i in range(len(model.encounters)):
            await msg.add_reaction(constants.NUMBER[i+1])

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Update the raid message"""
        channel = self.bot.get_channel(payload.channel_id)

        if isinstance(channel, discord.abc.PrivateChannel):
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
        if is_raid(message) and member != message.author:
            name = message.embeds[0].author.name

            if payload.emoji.name in constants.NUMBER:
                encounter = constants.NUMBER.index(payload.emoji.name)
                await self.set_encounter(encounter, name, message)
            elif payload.emoji.name == "\N{SKULL}":
                deleted = await self.delete_raid(guild, member, channel, message)

            if not deleted:
                try:
                    await message.remove_reaction(payload.emoji, member)
                except:
                    pass

    ####################################################################################################################
    async def set_encounter(self, encounter, name, message):
        """Updates raid help embed with current objective"""

        # Update raid message in place for a more seamless user experience
        model = RAIDS[name.replace("Raid: ", "")](encounter)
        raid_embed = await self.create_raid_embed(model)
        await message.edit(embed=raid_embed)

    ####################################################################################################################
    async def delete_raid(self, guild, member, channel, message):
        """Delete an event and update the events channel on success"""
        event_delete_role = get_event_delete_role(self.bot, guild)

        if member.permissions_in(channel).manage_guild  or (event_delete_role and member.top_role >= event_delete_role):
            deleted = await message.delete()
            if deleted:
                return True
        else:
            try:
                await member.send("You don't have permission to delete that event.")
            except:
                pass

    ####################################################################################################################
    async def create_raid_embed(self, raid_to_generate):
        """Create and return a Discord Embed object that represents the raid"""
        embed_msg = discord.Embed(color=constants.BLUE)
        embed_msg.title = raid_to_generate.title
        embed_msg.description = raid_to_generate.description

        if raid_to_generate.map:
            embed_msg.set_image(url=raid_to_generate.map)
        if raid_to_generate.thumbnail:
            embed_msg.set_thumbnail(url=raid_to_generate.thumbnail)
        if raid_to_generate.fields:
            for field in raid_to_generate.fields:
                embed_msg.add_field(name=field[0], value=field[1], inline=field[2])
        embed_msg.set_footer(text="\n\nReact with {} to remove this guide".format('\U0001f480'))
        embed_msg.set_author(name=f"Raid: {raid_to_generate.name}")
        return embed_msg
