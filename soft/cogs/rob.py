import random
import sqlite3
from discord.ext import commands
import discord

class Rob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, ctx, victim: commands.MemberConverter, amount: int):
        if amount < 1:
            await ctx.reply("You cannot rob less than 1.")
            return

        robber = ctx.author
        victim_id = victim.id
        robber_id = robber.id

        if victim_id == robber_id:
            embed = discord.Embed(title="Can't Rob Yourself", description="You fool, how can you rob yourself!", color=0xFF0000)
            await ctx.reply(embed=embed)
            return

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        try:
            # Start a database transaction
            db.execute("BEGIN")

            # Check if the victim exists in the database
            cursor.execute("SELECT wallet FROM main WHERE user_id = ?", (victim_id,))
            result = cursor.fetchone()

            if result is None:
                await ctx.reply("The victim does not have a wallet to rob.")
                return

            victim_wallet = result[0]

            # Check if the robber exists in the database
            cursor.execute("SELECT wallet FROM main WHERE user_id = ?", (robber_id,))
            result = cursor.fetchone()

            if result is None:
                await ctx.reply("You don't have a wallet to rob with.")
                return

            robber_wallet = result[0]

            # Check if the robber has enough money to make that rob
            if robber_wallet < amount:
                await ctx.reply("You don't have enough money to make that rob.")
                return

            # Check if the amount being robbed is greater than the victim's wallet balance
            if amount > victim_wallet:
                await ctx.reply("Cannot rob more than victim's wallet balance!")
                return

            # Deduct the amount from victim's wallet and add it to the robber's wallet
            victim_new_wallet = victim_wallet - amount
            robber_new_wallet = robber_wallet + amount

            # Update the victim's wallet and robber's wallet in a single transaction
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (victim_new_wallet, victim_id))
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (robber_new_wallet, robber_id))

            # Commit the transaction
            db.commit()

            await ctx.reply(f"{robber.name} robbed 🪙 {amount} from {victim.name}!")

        except Exception as e:
            await ctx.reply(f"An error occurred while trying to rob {victim.name}: {str(e)}")

        finally:
            cursor.close()
            db.close()


    @rob.error
    async def rob_error(self, ctx, error):
     if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Command on cooldown", description=f"Please try again in {int(error.retry_after)} seconds.", color=0xFF0000)
        embed.set_footer(text="Try again with a correct member name <@member>")
        await ctx.reply(embed=embed)
     elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Bad argument", description=str(error), color=0xFFFF00)
        embed.set_footer(text="Please provide a valid member and a positive integer amount.")
        await ctx.reply(embed=embed)
     elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Missing argument", description=f"You are missing the `{error.param.name}` argument. Please provide a valid member and a positive integer amount.", color=0xFFFF00)
        embed.set_footer(text="Correct command usage: `!rob <member> <amount>`")
        await ctx.reply(embed=embed)
     elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title="Permission denied", description="You do not have permission to use this command.", color=0xFF0000)
        await ctx.reply(embed=embed)
     else:
        embed = discord.Embed(title="Error", description=str(error), color=0xFF0000)
        await ctx.reply(embed=embed)


async def setup(bot):
   await bot.add_cog(Rob(bot))
