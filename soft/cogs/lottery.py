import random
import sqlite3
import discord
from discord.ext import commands


class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lottery(self, ctx, bet_amount: int):
        member = ctx.author

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        # Check if user has enough balance to place a bet
        cursor.execute(
            f"SELECT wallet FROM main WHERE user_id = {member.id}")
        wallet = cursor.fetchone()
        if wallet is None:
            wallet = (0,)
        if bet_amount > wallet[0]:
            await ctx.reply("You don't have enough balance to place a bet.")
            return

        # Place the bet and deduct from user's wallet
        cursor.execute(
            f"UPDATE main SET wallet = wallet - {bet_amount} WHERE user_id = {member.id}"
        )
        db.commit()

        # Generate lottery numbers
        lottery_numbers = random.sample(range(1, 51), 6)
        lottery_numbers_str = ", ".join(str(num) for num in lottery_numbers)

        # Determine payout
        winnings = 0
        if lottery_numbers == [7, 14, 21, 28, 35, 42]:
            winnings = bet_amount * 1500000
        elif lottery_numbers == [1, 2, 3, 4, 5, 6]:
            winnings = bet_amount * 100
        elif len(set(lottery_numbers).intersection(set([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]))) >= 3:
            winnings = bet_amount * 10

        # Update user's balance with winnings
        cursor.execute(
            f"UPDATE main SET wallet = wallet + {winnings} WHERE user_id = {member.id}"
        )
        db.commit()

        # Build and send response embed
        embed = discord.Embed(title=f"{member.display_name}'s Lottery Results", color=discord.Color.gold())
        embed.add_field(name="Lottery Numbers", value=lottery_numbers_str)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/536/536139.png")

        if winnings > 0:
            embed.add_field(name="Winnings", value=f"{winnings:,}")
        else:
            embed.add_field(name="Winnings", value="None :cry:")
        embed.set_footer(text="Lottery is drawn every day at 12:00 UTC.")
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Lottery(bot))
