import discord
from discord.ext import commands

class ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot 
  
  @commands.command()
  async def ping(self, ctx):
    """
       the bot to chek if it's online.

        Usage: $ping ["None"]
    """
    await ctx.reply("Pong")

async def setup(bot):
  await bot.add_cog(ping(bot))
