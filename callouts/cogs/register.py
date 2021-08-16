import pickle
import asyncio
import sys
import pydest
from discord.ext import commands
import discord


from cogs.utils.message_manager import MessageManager
from cogs.utils import constants


class Register(commands.Cog):

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot

    ####################################################################################################################
    @commands.command()
    @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def register(self, ctx):
        """Register your Destiny 2 account with the bot

        This command will let the bot know which Destiny 2 profile to associate with your Discord
        profile. Registering is a prerequisite to using any commands that require knowledge of your
        Destiny 2 profile.
        """
        manager = MessageManager(ctx)
        steam_name, xbox_name, psn_name, stadia_name, steam_id, xbox_id, psn_id, stadia_id = (None,)*8

        if not isinstance(ctx.channel, discord.abc.PrivateChannel):
            manager.add_messages_to_clean([ctx.message])
            await manager.clean_messages()

        registered_user_info = self.bot.db.get_user_by_discord_id(ctx.author.id)
        if registered_user_info:
            registration_msg = await manager.send_private_message("Lets update your registration")
            bungie_id = registered_user_info.get('bungie_id')
        else:
            # Get the user registered
            registration_msg = await manager.send_private_message("Enter your bungie id. It can be found at https://www.bungie.net/en/Profile/",
                                                                  attach_file=discord.File("registration_example.png"))
            res = await manager.get_next_private_message()
            if not res:
                return await manager.clean_messages()
            bungie_id = res.content

        await ctx.author.dm_channel.trigger_typing()
        user_info = await self.search_by_bungie_id(manager, bungie_id)

        if not user_info:
            await manager.send_private_message("Oops, something went wrong during registration. Please try again.")
            await registration_msg.delete()
            return await manager.clean_messages()
        
        # Save credentials and bungie ID
        bungie_id = user_info['bungieNetUser']['membershipId']
        self.bot.db.update_registration(bungie_id, ctx.author.id)

        # Fetch platform specific display names and membership IDs
        if not self.user_has_connected_accounts(user_info):
            await manager.send_private_message("Oops, you don't have any public accounts attached to your Bungie.net profile.")
            await registration_msg.delete()
            return await manager.clean_messages()

        primary_membership_id = user_info['primaryMembershipId']
        primary_membership_type = 0

        for entry in user_info['destinyMemberships']:
            membership_type = entry['membershipType']
            if entry['membershipId'] == primary_membership_id:
                primary_membership_type = membership_type
            if membership_type == 1:
                xbox_name = entry['displayName']
                xbox_id = entry['membershipId']
            elif membership_type == 2:
                psn_name = entry['displayName']
                psn_id = entry['membershipId']
            elif membership_type == 3:
                steam_name = entry['displayName']
                steam_id = entry['membershipId']
            elif membership_type == 5:
                stadia_name = entry['displayName']
                stadia_id = entry['membershipId']

        bungie_name = user_info['bungieNetUser']['displayName']
        self.bot.db.update_display_names(ctx.author.id, bungie_name, steam_name, xbox_name, psn_name, stadia_name)
        self.bot.db.update_membership_ids(ctx.author.id, steam_id, xbox_id, psn_id, stadia_id)
        self.bot.db.update_platform(ctx.author.id, primary_membership_type)

        # Get references to platform emojis
        platform_reactions = []
        if steam_name:
            platform_reactions.append(self.bot.get_emoji(constants.STEAM_ICON))
        if xbox_name:
            platform_reactions.append(self.bot.get_emoji(constants.XBOX_ICON))
        if psn_name:
            platform_reactions.append(self.bot.get_emoji(constants.PS_ICON))
        if stadia_name:
            platform_reactions.append(self.bot.get_emoji(constants.STADIA_ICON))
    
        # Display message with prompts to select a preferred platform
        e = self.registered_embed(bungie_name, steam_name, xbox_name, psn_name, stadia_name)
        platform_msg = await manager.send_private_embed(e)
        await registration_msg.delete()

        # If only one account is connected, set it as preferred (don't display reactions)
        platform_names = (steam_name, xbox_name, psn_name, stadia_name)
        if self.num_non_null_entries(platform_names) == 1:
            if steam_name:
                platform_id = 3
            elif xbox_name:
                platform_id = 1
            elif stadia_name:
                platform_id = 5
            else:
                platform_id = 2

            self.bot.db.update_platform(ctx.author.id, platform_id)
            return await manager.clean_messages()

        func = self.add_reactions(platform_msg, platform_reactions)
        self.bot.loop.create_task(func)

        def check_reaction(reaction, user):
            if reaction.message.id == platform_msg.id and user == ctx.author:
                for emoji in platform_reactions:
                    if reaction.emoji == emoji:
                        return True

        # Wait for platform reaction from user
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=120.0, check=check_reaction)
        except asyncio.TimeoutError:
            await platform_msg.delete()
            await manager.send_private_message("I'm not sure where you went. We can try this again later.")
            return await manager.clean_messages()

        # Save preferred platform
        platform = constants.PLATFORMS.get(reaction.emoji.name)
        self.bot.db.update_platform(ctx.author.id, platform)

        # Update message with preferred platform
        e = self.registered_embed(bungie_name, steam_name, xbox_name, psn_name, stadia_name, footer=True, platform=platform)
        await platform_msg.edit(embed=e)

        await manager.clean_messages()
        return self.bot.db.get_user_by_discord_id(ctx.author.id)

    ####################################################################################################################
    def registered_embed(self, bungie_name, steam_name, xbox_name, psn_name, stadia_name, footer=False, platform=None):
        """Create the embed that displays a user's connected accounts"""
        names = (steam_name, xbox_name, psn_name, stadia_name)
        e = discord.Embed(colour=constants.BLUE)
        e.title = "Registration Complete"

        if self.num_non_null_entries(names) != 1:
            e.description = "Please select the platform your cross-save characters are on.\n You can always change it by registering again!"
        else:
            e.description = "You have only one connected account, it has been set as your preferred platform."

        # If a preferred platform is already set, display it in bold
        if platform == 1:
            xbox_name = "**{}**".format(xbox_name)
        elif platform == 2:
            psn_name = "**{}**".format(psn_name)
        elif platform == 3:
            steam_name = "**{}**".format(steam_name)
        elif platform == 5:
            stadia_name = "**{}**".format(stadia_name)

        # Display connected accounts
        accounts = ""
        accounts += "{} {}\n".format(str(self.bot.get_emoji(constants.STEAM_ICON)), steam_name) if steam_name else ''
        accounts += "{} {}\n".format(str(self.bot.get_emoji(constants.XBOX_ICON)), xbox_name) if xbox_name else ''
        accounts += "{} {}\n".format(str(self.bot.get_emoji(constants.PS_ICON)), psn_name) if psn_name else ''
        accounts += "{} {}".format(str(self.bot.get_emoji(constants.STADIA_ICON)), stadia_name) if stadia_name else ''
        e.add_field(name="Connected Accounts", value=accounts)

        if footer:
            e.set_footer(text="Your preferred platform has been set!")

        return e

    ####################################################################################################################
    def user_has_connected_accounts(self, json):
        """Return true if user has connected destiny accounts"""
        if len(json['destinyMemberships']):
            return True

    ####################################################################################################################
    def num_non_null_entries(self, list):
        """Count the number of non null entries in a list"""
        count = 0
        for entry in list:
            if entry:
                count += 1
        return count

    ####################################################################################################################
    async def add_reactions(self, message, reactions):
        """Add platform reactions to message"""
        for icon in reactions:
            await message.add_reaction(icon)

    ####################################################################################################################
    async def search_by_bungie_id(self, manager, bungie_id):
        try:
            res = await self.bot.destiny.api.get_membership_data_by_id(bungie_id, membership_type=254)
        except pydest.PydestException:
            await manager.send_message("Sorry, I can't seem to search right now.")
            return await manager.clean_messages()
        except ValueError:
            await manager.send_message("Your username contains unsupported characters.")
            return await manager.clean_messages()

        if res['ErrorCode'] != 1:
            await manager.send_message("Sorry, I can't seem to search right now")
            return await manager.clean_messages()

        # Check how many results were found - we need at least one
        if not res['Response']:
            await manager.send_message("I didn't find any accounts that match your search.")
            return await manager.clean_messages()
        return res['Response']
