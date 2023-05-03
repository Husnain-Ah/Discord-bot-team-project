from typing_extensions import Self
import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_ready(self):
      print("welcome.py is online")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            embed = discord.Embed(title=f"Welcome {member.display_name}!",
                                  description="We're so glad you joined us!",
                                  color=discord.Color.purple())
            await channel.reply(embed=embed)

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None,):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            embed = discord.Embed(title=f"Hello {member.display_name}!",
                                  description="How are you today?",
                                  color=discord.Color.purple())
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=f"Hello {member.display_name}!",
                                  description="This feels familiar...",
                                  color=discord.Color.purple())
            await ctx.reply(embed=embed)
        self._last_member = member


    @commands.command()
    async def send(self, ctx, *, message):
        for member in ctx.guild.members:
            if member != self.bot.user:
                try:
                    await member.send(message)
                except Exception as e:
                    print(f"Failed to send message to {member}: {e}")
                    
        await ctx.reply(f"Message sent to {len(ctx.guild.members)-1} members.")



async def setup(bot):
    await bot.add_cog(Welcome(bot))
