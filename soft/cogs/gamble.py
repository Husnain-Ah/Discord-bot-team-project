import random
import sqlite3
from discord.ext import commands

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gamble(self, ctx, bet: int):
        if bet < 1:
            await ctx.reply("You cannot bet less than 1.")
            return

        user = ctx.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT wallet FROM main WHERE user_id = {user.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.reply("You don't have any money to gamble.")
            return

        wallet = result[0]

        if wallet < bet:
            await ctx.reply("You don't have enough money to make that bet.")
            return

        win = random.choice([True, False])

        if win:
            winnings = int(bet * 0.8)
            new_wallet = wallet + winnings
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (new_wallet, user.id))
            db.commit()
            await ctx.reply(f"You won 🪙 {winnings}!")
        else:
            new_wallet = wallet - bet
            cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (new_wallet, user.id))
            db.commit()
            await ctx.reply(f"You lost 🪙 {bet}!")




        cursor.close()
        db.close()

async def setup(bot):
   await bot.add_cog(Gamble(bot))