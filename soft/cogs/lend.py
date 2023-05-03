import sqlite3
import discord
from discord.ext import commands

class Lend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lendcooldown = {}

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def lend(self, ctx, borrower: commands.MemberConverter, amount: int):
        if amount < 1:
            await ctx.reply("You cannot lend less than 1.")
            return

        lender = ctx.author
        borrower_id = borrower.id
        lender_id = lender.id

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        # Check if the borrower exists in the database
        cursor.execute("SELECT * FROM main WHERE user_id = ?", (borrower_id,))
        result = cursor.fetchone()

        if result is None:
            await ctx.reply("The borrower does not have a wallet to receive the loan.")
            return

        borrower_wallet = result[1]

        # Check if the lender exists in the database
        cursor.execute("SELECT * FROM main WHERE user_id = ?", (lender_id,))
        result = cursor.fetchone()

        if result is None:
            await ctx.reply("You don't have a wallet to lend from.")
            return

        lender_wallet = result[1]

        # Check if the lender has enough money to make that loan
        if lender_wallet < amount:
            await ctx.reply("You don't have enough money to make that loan.")
            return

        # Add the amount to borrower's wallet and deduct it from the lender's wallet
        borrower_new_wallet = borrower_wallet + amount
        lender_new_wallet = lender_wallet - amount

        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (borrower_new_wallet, borrower_id))
        cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (lender_new_wallet, lender_id))

        db.commit()

        await ctx.reply(f"{lender.name} lent ${amount} to {borrower.name}!")

        cursor.close()
        db.close()

    @lend.error
    async def lend_error(self, ctx, error, member: discord.Member = None,):
     if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Command on cooldown", description=f"Please try again in {int(error.retry_after)} seconds.", color=0xFF0000)
        embed.set_footer(text="Try again with a correct member name <@member>")
        await ctx.reply(embed=embed)
     elif isinstance(error, commands.MemberNotFound):
        await ctx.reply("Could not find that member.")
     else:
        if member is None:
            error_embed = discord.Embed(
                title="Error", description="Sorry, please mention a member: `$lend @member 'amount'`", color=discord.Color.red())
            await ctx.reply(embed=error_embed)
            return





async def setup(bot):
   await bot.add_cog(Lend(bot))
