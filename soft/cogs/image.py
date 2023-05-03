import discord
import random
from googleapiclient.discovery import build
from discord.ext import commands


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "AIzaSyDllmsEYJNtdH5_NqaahaE6gik1S1O0WpA"  # Replace with your Google Custom Search API key
        self.cx = "16b40237238834bbd"  # Replace with your Google Custom Search Engine ID

    @commands.command(aliases=["img"])
    async def image(self, ctx, *, search):
        """
        Retrieve a image on the resquest of a user.

        Usage: $image ["Word"]
        """
        try:
            ran = random.randint(0, 9)
            resource = build("customsearch", "v1", developerKey=self.api_key).cse()
            result = resource.list(
                q=f"{search}", cx=self.cx, searchType="image"
            ).execute()
            url = result["items"][ran]["link"]
            embed = discord.Embed(
                color=0xFFC100, title=f"Here Your Image ({search})"
            )
            embed.set_image(url=url)
            embed.set_author(
                name=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.avatar.url,
            )

            await ctx.reply(embed=embed)
        except:
            error_embed = discord.Embed(
                title="Error",
                description="Sorry, there was an error while processing your request. Please make sure you entered the correct command: `$show or $showpic`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=error_embed)

   
async def setup(bot):
  await bot.add_cog(Image(bot))
