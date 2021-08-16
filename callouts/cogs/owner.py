from discord.ext import commands

from cogs.utils.message_manager import MessageManager
from cogs.utils import constants


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    async def pm(self, ctx, user_id: str, *message):
        """Send a PM via the bot to a user given their ID"""
        manager = MessageManager(ctx)
        user = [i for i in self.bot.users if i.display_name == "cmyager"]
        if not user:
            return
        user = self.bot.get_user(int(user[0].id))

        if ctx.author.id not in constants.MODS:
            return

        if len(message) == 0:
            await manager.send_message("You forgot to include your message!")
            return await manager.clean_messages()

        response = "You have received a message from my developer:\n\n**"
        for word in message:
            response += "{} ".format(word)
        response += ("**\n\nYour response will not be tracked here.")
        try:
            await user.send(response)
        except:
            await manager.send_message('Could not PM user with ID {}'.format(user_id))
        else:
            await manager.send_message('PM successfully sent.')
        await manager.clean_messages()


    @commands.command(hidden=True)
    async def broadcast(self, ctx, *, message):
        """Send a message to the owner of every server the bot belongs to"""
        manager = MessageManager(ctx)

        if ctx.author.id not in constants.OWNERS:
            return

        count = 0
        for guild in self.bot.guilds:
            try:
                await guild.owner.send(message)
            except:
                pass
            else:
                count+= 1

        await manager.send_message("Broadcast message sent to **{}** users".format(count))
        await manager.clean_messages()


    @broadcast.error
    async def broadcast_error(self, ctx, error):
        manager = MessageManager(ctx)
        await manager.send_message("You didn't include a broadcast message")
        return await manager.clean_messages()
