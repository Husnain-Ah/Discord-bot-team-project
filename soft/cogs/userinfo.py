import discord
from discord.ext import commands
from datetime import datetime


class Userinfo(commands.Cog):
    """
    Retrieve information about a specific member on the server.

    Usage: $userinfo [@member]
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            error_embed = discord.Embed(
                title="Error", description="Sorry, please mention a member: `$userinfo @member`", color=discord.Color.red())
            await ctx.reply(embed=error_embed)
            return

        join_date = member.joined_at.strftime('%B %d, %Y')
        create_date = member.created_at.strftime('%B %d, %Y')
        booster_since = member.premium_since.strftime(
            '%B %d, %Y') if member.premium_since else "Not currently boosting this guild."

        embed = discord.Embed(title="User Info", color=discord.Color.green())
        embed.add_field(name="Username:", value=member.mention, inline=False)
        embed.add_field(name="Discriminator:",
                        value=member.discriminator, inline=False)
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Current status", value=member.status, inline=False)
        embed.add_field(name="Booster Since", value=booster_since, inline=False)
        embed.add_field(name="Highest Role", value=member.top_role, inline=False)
        embed.add_field(name="Joined At", value=join_date, inline=False)
        embed.add_field(name="Account Created At", value=create_date, inline=False)

        embed.set_author(
            name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed)


async def setup(bot):
   await bot.add_cog(Userinfo(bot))

