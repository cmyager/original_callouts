# pylint: disable=no-member
import os
import datetime
import asyncio
from pathlib import Path
import sys
import pydest
from discord.ext import commands, tasks
import discord
from time import sleep
from cogs.utils.message_manager import MessageManager
from collections import namedtuple
from cogs.utils import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FCTX = namedtuple('FCTX', ['channel', 'author', 'message', 'guild', 'bot'])

class Report(commands.Cog):

    ####################################################################################################################
    def __init__(self, bot):
        self.bot = bot
        self.chromeOptions = Options()
        self.chromeOptions.headless = True
        self.executable_path='/home/callouts/callouts/drivers/chromedriver'
        self.channel_name = "raid-reports"
        self.clean_channel.start()
        self.clean_images.start()
        self.get_report_in_progress = False
        self.report_watch_list = []
        self.report_watch_start_time = None

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.get_reports_channel(guild=guild)

    ####################################################################################################################
    @tasks.loop(hours=24)
    async def clean_channel(self):
        for guild in self.bot.guilds:
            report_channel = await self.get_reports_channel(guild=guild)
            all_attachments = []
            async for message in report_channel.history():
                delete_message = False

                attachments = [i.filename for i in message.attachments]
                new_attachments = [i for i in attachments if i not in all_attachments]
                all_attachments += new_attachments

                if message.author.name != "Callouts":
                    delete_message = True
                elif not message.attachments:
                    delete_message = True
                elif len(attachments) != len(new_attachments):
                    delete_message = True
                elif datetime.datetime.now() - message.created_at > datetime.timedelta(days=30):
                    delete_message = True
               
                if delete_message is True:
                    await message.delete()

            messages = await report_channel.history().flatten()
            [await i.clear() for sublist in messages for i in sublist.reactions]
            if messages:
                await messages[0].add_reaction("\N{HEAVY PLUS SIGN}")

    ####################################################################################################################
    @tasks.loop(hours=720)
    async def clean_images(self):
        for item in Path("images").glob('*'):
            if item.is_file() and item.name != "0.png":
                create_date = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                if datetime.datetime.now() - create_date > datetime.timedelta(days=30):
                    os.remove(str(item))

    ####################################################################################################################
    @clean_channel.before_loop
    async def before_clean_channel(self):
        await self.bot.wait_until_ready()

    ####################################################################################################################
    @tasks.loop(minutes=1.0)
    async def report_watch(self):
        if self.report_watch_start_time is None:
            self.report_watch_start_time = datetime.datetime.now()
        current_delta = datetime.datetime.now() - self.report_watch_start_time
        if current_delta.total_seconds() > 1800:
            member = self.report_watch_list[0]
            user_info = self.bot.db.get_user_by_discord_id(member.id)
            await self.get_report(user_info, member.guild, filter=True)

    ####################################################################################################################
    @report_watch.before_loop
    async def before_report_watch(self):
        await self.bot.wait_until_ready()

    ####################################################################################################################
    @commands.command()
    @commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
    async def report(self, ctx):
        """Posts your most recent raid report."""
        manager = MessageManager(ctx)

        if not isinstance(ctx.channel, discord.abc.PrivateChannel) and ctx.message:
            manager.add_messages_to_clean([ctx.message])
            await manager.clean_messages()

        user_info = self.bot.db.get_user_by_discord_id(ctx.author.id)
        if not user_info:
            # Get the user registered 
            user_info = await self.bot.cogs["Register"].register(ctx)
        if not user_info:
            return

        await ctx.channel.trigger_typing()
        return await self.get_report(user_info, ctx.guild, ctx.channel)

    ####################################################################################################################
    async def get_report(self, user_info, guild=None, pm_channel=None, filter=False):
        try:
            if self.get_report_in_progress is True:
                raise Exception
            self.get_report_in_progress = True
            # Save credentials and bungie ID
            if guild is not None:
                reports_channel = await self.get_reports_channel(guild)
            elif pm_channel is not None:
                reports_channel = pm_channel
            else:
                raise Exception("guild or channel must be provided")

            bungie_id = None
            membership_type = user_info.get("platform")
            if membership_type == 1:
                bungie_id = user_info.get('xbox_id')
            elif membership_type == 2:
                bungie_id = user_info.get('psn_id')
            elif membership_type == 3:
                bungie_id = user_info.get('steam_id')
            elif membership_type == 5:
                bungie_id = user_info.get('stadia_id')
            # Fetch characters
            try:
                res = await self.bot.destiny.api.get_profile(membership_type, bungie_id, ["Characters"])
            except:
                await reports_channel.send("I can't seem to connect to Bungie right now. Try again later.")

            if res['ErrorCode'] != 1:
                await reports_channel.send("Oops, something went wrong. Please try again.")

            character_ids = list(res['Response']['characters']['data'])

            instance_ids = [0]
            for character_id in character_ids:
                res = await self.bot.destiny.api.get_activity_history(membership_type, bungie_id, character_id, count=1, mode=4)
                if res["Response"]:
                    instance_id = res['Response']['activities'][0]['activityDetails']['instanceId']
                    completed = res['Response']['activities'][0]['values']['completed']['basic']['displayValue']

                    if filter is True:
                        period = res['Response']['activities'][0]['period']
                        period = datetime.datetime.strptime(period, '%Y-%m-%dT%H:%M:%SZ')
                        delta = datetime.datetime.now() - period
                        if delta.days > 1:
                            instance_id = 0

                    if completed == "Yes":
                        instance_ids.append(int(instance_id))
                    else:
                        # instance_ids.append(int(instance_id))
                        pass

            instance_ids.sort()
            recent_raid_id = instance_ids[-1]
            image_name = f"{recent_raid_id}.png"
            image_path = f"images/{image_name}"

            # Get all messages from the reports channel
            messages = await reports_channel.history().flatten()
            # Get all attachment names
            attachments = [i.filename for sublist in messages for i in sublist.attachments]
            # Only post new reports
            if image_name in attachments:
                raise Exception()

            if pm_channel is None and os.path.isfile(image_path):
                raise Exception()

            users = ""
            if guild is not None:
                pgcr = await self.bot.destiny.api.get_post_game_carnage_report(recent_raid_id)
                if pgcr["Response"]:
                    pgcr = pgcr["Response"]["entries"]
                    for player in pgcr:
                        player = player["player"]["destinyUserInfo"]
                        membership_type = int(player["membershipType"])
                        membership_id = int(player["membershipId"])
                        raid_user_info = self.bot.db.get_user_by_platform_id(membership_type, membership_id)
                        if raid_user_info:
                            user_id = raid_user_info['user_id']
                            member = guild.get_member(user_id)
                            if member:
                                users += f"<@{user_id}> "

            try:
                driver = None
                if os.path.isfile(image_path) is False:
                    driver = webdriver.Chrome(executable_path=self.executable_path,
                                            options=self.chromeOptions)
                    # Set the dark theme
                    driver.get("https://raid.report/settings")
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "MuiFormControlLabel-root")))
                    for element in driver.find_elements_by_class_name("MuiFormControlLabel-root"):
                        if element.text == "Dark":
                            element.click()
                    # Get the report
                    driver.get(f"https://raid.report/pgcr/{recent_raid_id}")
                    driver.set_window_position(0, 0)
                    driver.set_window_size(1024, 768)
                    # Wait for the page to load
                    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "pgcr-table")))
                    sleep(2)
                    # Delete the ad
                    driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""",
                                        driver.find_element_by_class_name('jss1'))
                    # Find the report
                    element = driver.find_element_by_class_name("side-container")
                    # Screenshot the report
                    element.screenshot(image_path)

                # Get all messages from the reports channel
                # messages = await reports_channel.history().flatten()

                # # Get all attachment names
                # attachments = [i.filename for sublist in messages for i in sublist.attachments]
                
                # Only post new reports
                if image_name not in attachments:
                    msg = await reports_channel.send(users ,file=discord.File(image_path))
                    # Remove old react from the previous event messages
                    if not isinstance(reports_channel, discord.abc.PrivateChannel):
                        # Remove reactions on reports channel
                        [await i.clear() for sublist in messages for i in sublist.reactions]
                        await msg.add_reaction("\N{HEAVY PLUS SIGN}")
            except Exception as E:
                print(E)
                await reports_channel.send("Oops, something went wrong. Please try again.")
            finally:
                if driver is not None:
                    driver.quit()
        except:
            pass
        finally:
            self.get_report_in_progress = False
        return True

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """If a reaction represents requesting a new report do it"""
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

        # We check that the user is not the message author as to not count
        # the initial reactions added by the bot as being indicative of a report request
        if member != message.author and channel.id == (await self.get_reports_channel(guild)).id:
            if payload.emoji.name == "\N{HEAVY PLUS SIGN}":
                try:                    
                    await message.remove_reaction(payload.emoji, member)
                    ctx = FCTX(channel, member, None, guild, self.bot)
                    await self.report(ctx)
                except:
                    pass

    ####################################################################################################################
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user_info = self.bot.db.get_user_by_discord_id(member.id)
        if not user_info or user_info.get("bungie_id") is None:
            return
        if after.channel is not None and "Raid" in after.channel.name:
            if member not in self.report_watch_list:
                self.report_watch_list.append(member)

        elif before.channel is not None and "Raid" in before.channel.name:
            if member in self.report_watch_list:
                self.report_watch_list.remove(member)
        else:
            return

        if self.report_watch_list:
            if self.report_watch.is_running() is False:
                self.report_watch.start()
        else:
            self.report_watch_start_time = None
            if self.report_watch.is_running():
                self.report_watch.stop()

    ####################################################################################################################
    async def get_reports_channel(self, guild):
        """Return the reports channel if it exists, otherwise create one and return it"""
        for channel in guild.channels:
            if channel.name == self.channel_name:
                return channel

        # Need to make sure the bot can still send messages in the reports channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=True),
            guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True)
        }
        return await guild.create_text_channel(self.channel_name, overwrites=overwrites)
