from discord.ext import commands
import discord
import asyncio

class TimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeouts = set()

    @commands.command(aliases=["out"])
    @commands.has_role("Moderator")
    async def timeout(self, ctx, user: discord.Member, timeout_duration: int):
        """
        Timeout a member for a certain amount of time.

        Usage: $timeout [@member]
        """
        role = discord.utils.get(ctx.guild.roles, name='Timeout')
        if role is not None:
            await user.add_roles(role)
            await ctx.send(f'{user.mention} has been timed out for {timeout_duration} seconds.')
            await user.send(f'You have been timed out for {timeout_duration} seconds. You will not be able to send messages in the server until the timeout expires.')
            self.timeouts.add(user.id)
            await asyncio.sleep(timeout_duration)
            await user.remove_roles(role)
            self.timeouts.remove(user.id)
            await ctx.send(f'{user.mention} has been un-timed out.')
        else:
            await ctx.reply("Timeout role not found. Please create a role called 'Timeout' and try again.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.timeouts:
            await message.delete()

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply("You do not have permission to use this command.")

    
async def setup(bot):
    await bot.add_cog(TimeoutCog(bot))



