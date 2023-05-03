import asyncio
import discord
from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Add user's experience
        if message.author not in self.users:
            self.users[message.author] = 0
        self.users[message.author] += 10

        # Check if user has enough experience to level up
        level = int(self.users[message.author] / 100) + 1
        if self.users[message.author] % 100 == 0 and level <= 10:
            await message.channel.send(f'{message.author.mention} has leveled up to level {level}!')

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        """
        Check the level of a member.

        Usage: $level [@member]
        """
        if member is None:
            member = ctx.author

        if member not in self.users:
            error_embed = discord.Embed(
                title="Error", description=f"{member.display_name} has not earned any experience yet.", color=discord.Color.red())
            await ctx.reply(embed=error_embed)
            return

        level = int(self.users[member] / 100) + 1
        xp_needed = level * 100 - self.users[member]
        progress_bar = '🟩' * int(self.users[member] / (level * 10)) + '🟦' * int(10 - self.users[member] / (level * 10))
        footer_text = "stop looking"

        embed = discord.Embed(title=f"Level {level}", color=discord.Color.green())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Experience", value=f"{self.users[member]} XP", inline=False)
        embed.add_field(name="Progress", value=f"{progress_bar} ({self.users[member]}/{level * 100})", inline=False)
        embed.add_field(name="XP to Next Level", value=f"{xp_needed} XP", inline=False)
        embed.set_footer(text=footer_text)

        await ctx.reply(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        """
        Display the top 10 users based on experience.
        """
        sorted_users = sorted(self.users.items(), key=lambda x: x[1], reverse=True)[:10]

        embed = discord.Embed(title="Leaderboard", color=discord.Color.blue())
        for i, (user, xp) in enumerate(sorted_users):
            embed.add_field(name=f"{i+1}. {user.display_name}", value=f"{xp} XP", inline=False)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Level(bot))
