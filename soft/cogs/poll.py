import asyncio
import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *args):
        """
        Give a question and the members can react.

        Usage: $poll [Question?]
        """
        question = ' '.join(args)
        poll_message = f'Poll: {question}\n\nReact with 👍 to vote yes and 👎 to vote no.'
        poll_embed = discord.Embed(description=poll_message, color=discord.Color.red())

        # Add reactions to message
        await ctx.send(embed=poll_embed)
        async for message in ctx.history(limit=1):
            poll_message = message
            break
        await poll_message.add_reaction('👍')
        await poll_message.add_reaction('👎')

        # Define timeout and vote tracking
        timeout = 60  # Timeout in seconds
        votes = {'👍': 0, '👎': 0}

        # Wait for reactions
        def check(reaction, user):
            return user != self.bot.user and reaction.emoji in ['👍', '👎']

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=timeout, check=check)
            while reaction:
                votes[reaction.emoji] += 1
                reaction, user = await self.bot.wait_for('reaction_add', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            pass

        # Display results
        results_message = f'Poll results: {votes["👍"]} votes for yes, {votes["👎"]} votes for no.'
        results_embed = discord.Embed(description=results_message, color=discord.Color.red())
        await ctx.send(embed=results_embed)
        
async def setup(bot):
  await bot.add_cog(Poll(bot))